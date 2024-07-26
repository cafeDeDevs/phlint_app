import os
import hmac
import base64
from hashlib import sha256
from time import time

from django.middleware.csrf import get_token


# NOTE: Helper function for setting cookies (consider moving into separate file/Class)
def set_authentication_cookies(response, access_token, refresh_token, request):
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        samesite='None',
        secure=True,
        path='/',
    )
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        samesite='None',
        secure=True,
        path='/',
    )
    # NOTE: Sets the csrftoken as cookie by default
    get_token(request)
    return response


def remove_authenticated_cookies(response):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    response.delete_cookie('csrftoken')
    response.delete_cookie('sessionid')
    return response


def generate_sha256_hash(email):
    secret_key = os.urandom(32)
    timestamp = str(int(time())).encode('utf-8')
    message = email.encode('utf-8') + timestamp
    signature = hmac.new(secret_key, message, sha256).digest()
    token = base64.urlsafe_b64encode(message + signature).decode('utf-8')
    return token
