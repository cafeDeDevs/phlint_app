# TODO: Add note of logger in a best_practices.md doc
# TODO: Move Routes into respective alternative files
# (i.e. tidy up, all functions within single file should relate to auth, gallery, etc. ...)

import base64
import logging
import boto3
import requests

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.csrf import csrf_protect

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from social_django.utils import psa

from users.serializers import UserSerializer

from users.utils.auth_utils import set_authentication_cookies, remove_authenticated_cookies
from users.utils.s3_utils import grab_file_list

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_gallery_test(request) -> Response:
    s3_client = boto3.client('s3')
    try:
        file_list = grab_file_list()
        image_files = []

        if len(file_list) != 0:
            for file in file_list:
                if '/' in file:
                    file_obj = s3_client.get_object(
                        Bucket='phlint-app-s3-test', Key=file)
                    image_data = base64.b64encode(
                        file_obj['Body'].read()).decode('utf-8')
                    image_files.append(image_data)
        else:
            return Response({'message': 'No Images In Your Gallery Found.'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(
            {
                'message':
                'Images Retrieved From S3 And Sent To Client Successfully.',
                'imagesAsBase64': image_files
            },
            status=status.HTTP_200_OK)
    except Exception as e:
        logging.error(e)
        return Response(
            {
                'message':
                'An Error Occurred While Trying To Retrieve Your Gallery'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request, backend) -> Response:
    try:
        response = Response({'message': 'User logged out successfully'},
                            status=status.HTTP_200_OK)
        remove_authenticated_cookies(response)
        Token.objects.filter(user=request.user).delete()  #type:ignore
        django_logout(request)
        return response
    except Exception as e:
        logger.error("Logout error: %s", str(e))
        return Response({'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def register_by_access_token(request, backend) -> Response:
    code = request.data.get('code')
    if not code:
        logger.warning("Request does not have OAuth code")
        return Response({'error': 'No OAuth code provided.'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
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
        refresh_token = tokens.get('refresh_token')
        user = request.backend.do_auth(access_token)

        if user:
            user_data = {
                'user_name': user.email,
                'user_email': user.email,
            }

            serializer = UserSerializer(data=user_data)
            existing_user = serializer.get_user_by_email(  #type:ignore
                data=user_data)
            if existing_user is not None:
                res = Response(
                    {
                        'message':
                        'Sign Up Failed. User Already Exists. Please Login.'
                    },
                    status=status.HTTP_409_CONFLICT)
                logger.warning(
                    "%s attempted to sign up, but already has account",
                    user.email)
                return res
            if serializer.is_valid():
                serializer.save()

            token, _ = Token.objects.get_or_create(user=user)  # type:ignore
            login(request, user)
            res = Response(
                {
                    'message': 'User Authenticated, setting credentials',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                },
                status=status.HTTP_200_OK,
            )
            res = set_authentication_cookies(res, token.key, refresh_token,
                                             request)

            logger.info("%s successful signed up", user.email)
            return res
        else:
            logger.warning("python social auth unable to authenticate user")
            return Response(
                {'error': 'User Not Found By OAuth Code'},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        logger.error("%s Uncaught Exception Error:", str(e))
        return Response({'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def login_by_access_token(request, backend) -> Response:
    code = request.data.get('code')
    if not code:
        logger.warning("Request does not have OAuth code")
        return Response({'error': 'No OAuth code provided.'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
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
        refresh_token = tokens.get('refresh_token')
        user = request.backend.do_auth(access_token)

        if user:
            user_data = {
                'user_name': user.email,
                'user_email': user.email,
            }

            serializer = UserSerializer(data=user_data)
            existing_user = serializer.get_user_by_email(  # type:ignore
                data=user_data)
            if existing_user is None:
                res = Response(
                    {
                        'message':
                        'Login Failed. User Does Not Exist. Please Sign Up.'
                    },
                    status=status.HTTP_401_UNAUTHORIZED)
                logger.warning(
                    "%s attempted to login, but does not yet have an account",
                    user.email)
                return res

            token, _ = Token.objects.get_or_create(user=user)  # type:ignore
            login(request, user)

            res = Response(
                {
                    'message': 'User Is Authenticated, Logging In...',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                },
                status=status.HTTP_200_OK,
            )
            res = set_authentication_cookies(res, token.key, refresh_token,
                                             request)

            logger.info("%s is successfully authenticated, logging in...",
                        user.email)
            return res
        else:
            logger.warning("python social auth unable to find user")
            return Response(
                {'message': 'User Not Found in Database'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    except Exception as e:
        logger.error("%s Uncaught Exception Error:", str(e))
        return Response({'message': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_protect
def authentication_test(request) -> Response:
    if isinstance(request.user, AnonymousUser):
        logger.warning("User attempted to login as AnonymousUser")
        return Response(
            {"message": "Access forbidden. You are not authenticated."},
            status=status.HTTP_401_UNAUTHORIZED)

    logger.info("%s successfully authenticated", request.user)
    return Response(
        {'message': "User successfully authenticated"},
        status=status.HTTP_200_OK,
    )
