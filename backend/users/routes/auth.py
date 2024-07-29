# TODO: Refactor so that repeated declarations
# and logic is abstracted as dicts, lists, or helper funcs
# TODO: Remove all #type:ignore using proper type checking
import logging

import redis
import requests
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from social_django.utils import psa

from users.serializers import *
from users.utils.auth_utils import *

logger = logging.getLogger(__name__)

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT,
                                   password=settings.REDIS_PASS,
                                   db=0)


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

            user_serializer = UserSerializer(data=user_data)
            existing_user = user_serializer.get_user_by_email(  #type:ignore
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
            # NOTE: If the user_serializer receives the appropriate data,
            # then the following series of table populations execute,
            # creating default data for the Albums, Photos, and Networks table
            # i.e. the user gets one new album, photo, and network
            # they are the owner/participant of
            if user_serializer.is_valid():
                # TODO: Most of this needs a helper function
                new_user = user_serializer.save()
                # TODO: Address need for proper s3_url in
                # albums_data and photos_data and save via boto3
                albums_data = {
                    'title': 'default_album',
                    's3_url': 'https://fake_for_now.com',
                    'is_private': False,
                    'user_id': new_user.id
                }
                album_serializer = AlbumsSerializer(data=albums_data)
                new_album = album_serializer.create_album(
                    data=albums_data)  #type:ignore
                photos_data = {
                    's3_url': 'https://fake_for_now.com',
                    'album_id': new_album.id,
                }
                photo_serializer = PhotosSerializer(data=photos_data)
                photo_serializer.create_photo(data=photos_data)
                networks_data = {
                    'founder_id': new_user.id,
                    'user_id': new_user.id,
                    'album_id': new_album.id,
                }
                network_serializer = NetworksSerializer(data=networks_data)
                network_serializer.create_network(data=networks_data)

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

            user_serializer = UserSerializer(data=user_data)
            existing_user = user_serializer.get_user_by_email(  # type:ignore
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


# TODO: Get to this later
# NOTE: Don't use default_token_generator, we'll be writing our own implementation
#  @api_view(['GET'])
#  @permission_classes([AllowAny])
#  def activate(request, uidb64, token):
#  try:
#  user = get_object_or_404(User, pk=uidb64)
#  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#  user = None

#  if user is not None and default_token_generator.check_token(user, token):
#  user.is_active = True
#  user.save()
#  return Response({'message': 'Account activated!'},
#  status=status.HTTP_200_OK)
#  else:
#  return Response({'message': 'Activation link is invalid!'},
#  status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def email_registration_view(request) -> Response:
    try:
        serializer = EmailRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']  #type:ignore

            token = generate_sha256_hash(email)

            # NOTE: Persists key/value pair associatin raw string email with token for 120 seconds
            redis_instance.set(f'signup_token_for_{email}', token, ex=120)
            # TODO: Remove later, this is just a demonstration
            token_value = redis_instance.get(f'signup_token_for_{email}')
            print(token_value)

            # activation_link = f'http://localhost:5173?token={token}'
            
            activation_link = f'http://localhost:5173/onboarding/?token={token}'
            
            # TODO: replace this with a template .html file,
            # and spruce it up with some nice styling
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
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=message,
            )
            res = Response({'message': 'Email sent!'},
                           status=status.HTTP_200_OK)
        else:
            res = Response(serializer.errors,
                           status=status.HTTP_400_BAD_REQUEST)
        return res
    except Exception as e:
        logger.error("%s Uncaught Exception Error:", str(e))
        return Response({'message': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
