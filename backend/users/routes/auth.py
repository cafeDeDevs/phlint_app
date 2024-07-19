import logging
import requests

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse 

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from social_django.utils import psa

from users.serializers import UserSerializer, EmailRegistrationSerializer
from django.core.mail import send_mail

from users.utils.auth_utils import *

logger = logging.getLogger(__name__)


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



@api_view(['GET'])
@permission_classes([AllowAny])
def activate(request, uidb64, token):
    try:
        user = get_object_or_404(User, pk=uidb64)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'message': 'Account activated!'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Activation link is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
@permission_classes([AllowAny])
def email_registration_view(request):
    serializer = EmailRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']

        user, created = User.objects.get_or_create(username=email, email=email)
        if created:
            user.is_active = False
            user.save()
        token = default_token_generator.make_token(user)
        activation_link = f'http://localhost:5173?token={token}&user_id={user.pk}'


        message = f"""
        <html>
        <body>
            <p>Thanks For Signing Up for Phlint! Please click on the button below to complete your sign up process!</p>
            <a href="{activation_link}" style="padding: 10px 20px; color: white; background-color: blue; text-decoration: none; border-radius: 5px;">Complete Sign Up</a>
        </body>
        </html>
        """

        send_mail(
            "Email verification",
            "Text version.",
            "from@example.com",
            [email],
            fail_silently=False,
            html_message=message,
        )
        return Response({'message': 'Email sent!'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
