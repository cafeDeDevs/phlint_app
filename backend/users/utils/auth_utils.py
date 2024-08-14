import hmac
import logging
import os
import re
from base64 import b64decode, b64encode, urlsafe_b64encode
from hashlib import scrypt, sha256
from time import time

import redis
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from django.conf import settings
from django.middleware.csrf import get_token
from rest_framework.response import Response


def set_authentication_cookies(
    response, access_token, refresh_token, request
) -> Response:
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="None",
        secure=True,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="None",
        secure=True,
        path="/",
    )
    # NOTE: Sets the csrftoken as cookie by default
    get_token(request)
    return response


def remove_authentication_cookies(response) -> Response:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("csrftoken")
    response.delete_cookie("sessionid")
    return response


def generate_sha256_hash(email) -> str:
    secret_key = os.urandom(32)
    timestamp = str(int(time())).encode("utf-8")
    message = email.encode("utf-8") + timestamp
    signature = hmac.new(secret_key, message, sha256).digest()
    token = urlsafe_b64encode(message + signature).decode("utf-8")
    return token


# AES Encryption/Decryption Algorithms from boot.dev
# https://blog.boot.dev/cryptography/aes-256-cipher-python-cryptography-examples/
def encrypt(plain_text, password) -> str:
    # generate a random salt
    salt = get_random_bytes(AES.block_size)

    # use the Scrypt KDF to get a private key from the password
    private_key = scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # encrypt the plain text
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, "utf-8"))

    # concatenate all parts into a single string
    encrypted_data = (
        b64encode(salt).decode("utf-8")
        + "::"
        + b64encode(cipher_text).decode("utf-8")
        + "::"
        + b64encode(cipher_config.nonce).decode("utf-8")
        + "::"
        + b64encode(tag).decode("utf-8")
    )
    return encrypted_data


def decrypt(encrypted_data, password) -> str:
    # split the string back into its components
    salt, cipher_text, nonce, tag = encrypted_data.split("::")

    # decode the components from base64
    salt = b64decode(salt)
    cipher_text = b64decode(cipher_text)
    nonce = b64decode(nonce)
    tag = b64decode(tag)

    # generate the private key from the password and salt
    private_key = scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text and verify the tag
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted.decode("utf-8")


# NOTE: user_name must be at least 5 characters
# NOTE: Password must be at last 10 characters,
# have at least one uppercase character, one symbol, and one number
user_name_pattern = re.compile(r"^.{5,}$")
password_pattern = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=[\]{};:\'"\\|,.<>/?]).{10,}$'
)

logger = logging.getLogger(__name__)

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASS,
    db=0,
)
