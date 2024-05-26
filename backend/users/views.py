import requests
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.conf import settings
from django.middleware.csrf import get_token
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.csrf import csrf_protect

from social_django.utils import psa
from requests.exceptions import HTTPError


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


# NOTE: Currently somewhat of a hack using python's native requests lib,
# there is probably a better way using the social_auth.core
@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def register_by_access_token(request, backend):
    code = request.data.get('code')
    if not code:
        return Response({'error': 'No OAuth code provided.'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        # NOTE: Consider moving these settings into separate file/Class
        token_url = 'https://www.googleapis.com/oauth2/v4/token'
        data = {
            'code': code,
            'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            'redirect_uri': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }

        response = requests.post(token_url, data=data)

        if response.status_code != 200:
            return Response({'error': 'Failed to get tokens from Google.'},
                            status=response.status_code)

        tokens = response.json()
        access_token = tokens.get('access_token')
        # TODO: refresh_token should be set in key/value store (i.e. redis cache)
        # and used to grab new access_token when access_token is expired
        # TODO: refresh_token could not exist, handle exception, but don't return
        refresh_token = tokens.get('refresh_token')
        user = request.backend.do_auth(access_token)

        if user:
            # TODO: Use the user.email to sign up/set user as logged in
            #  print('user.email :=>', user.email)

            token, _ = Token.objects.get_or_create(user=user)
            res = Response(
                {'msg': 'User Authenticated, setting credentials'},
                status=status.HTTP_200_OK,
            )
            res = set_authentication_cookies(res, token.key, refresh_token,
                                             request)
            return res
        else:
            return Response(
                {'error': 'User Not Found By OAuth Code'},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        return Response({'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# TODO: redirect to get new access_token if access_token is expired via refresh_token
@api_view(['POST'])
@csrf_protect
def authentication_test(request):
    #  print(request.user)
    if isinstance(request.user, AnonymousUser):
        return Response(
            {"error": "Access forbidden. You are not authenticated."},
            status=status.HTTP_401_UNAUTHORIZED)
    return Response(
        {'message': "User successfully authenticated"},
        status=status.HTTP_200_OK,
    )
