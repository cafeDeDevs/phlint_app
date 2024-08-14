# TODO: Refactor so that repeated declarations
# and logic is abstracted as dicts, lists, or helper funcs
# TODO: Remove all #type:ignore using proper type checking
import jwt
import requests
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from social_django.utils import psa
from users.models import User
from users.serializers import *
from users.utils.auth_utils import *


@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request, backend) -> Response:
    try:
        response = Response(
            {"message": "User logged out successfully"},
            status=status.HTTP_200_OK,
        )
        remove_authentication_cookies(response)
        logout(request)
        return response
    except Exception as e:
        logger.error("Logout error: %s", str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([AllowAny])
@psa()
def register_by_access_token(request, backend) -> Response:
    code = request.data.get("code")
    if not code:
        logger.warning("Request does not have OAuth code")
        return Response(
            {"error": "No OAuth code provided."}, status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        token_url = "https://www.googleapis.com/oauth2/v4/token"
        data = {
            "code": code,
            "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            "redirect_uri": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = requests.post(token_url, data=data)

        if response.status_code != 200:
            return Response(
                {"error": "Failed to get tokens from Google."},
                status=response.status_code,
            )

        tokens = response.json()
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")

        user = request.backend.do_auth(access_token)

        if user:
            user_data = {
                "user_name": user.email,
                "user_email": user.email,
            }

            user_serializer = UserSerializer(data=user_data)
            existing_user = user_serializer.get_user_by_email(data=user_data)

            if existing_user is not None:
                res = Response(
                    {"message": "Sign Up Failed. User Already Exists. Please Login."},
                    status=status.HTTP_409_CONFLICT,
                )
                logger.warning(
                    "%s attempted to sign up, but already has account", user.email
                )
                return res

            if user_serializer.is_valid():
                new_user = user_serializer.save()

                # Create default album, photo, and network
                albums_data = {
                    "title": "default_album",
                    "album_name": f"{user}/default/",
                    "is_private": False,
                    "user_id": new_user.id,
                }
                album_serializer = AlbumsSerializer(data=albums_data)
                new_album = album_serializer.create_album(data=albums_data)

                photos_data = {
                    "file_name": "default.jpg",
                    "album_id": new_album.id,
                }
                photo_serializer = PhotosSerializer(data=photos_data)
                photo_serializer.create_photo(data=photos_data)

                networks_data = {
                    "founder_id": new_user.id,
                    "user_id": new_user.id,
                    "album_id": new_album.id,
                }
                network_serializer = NetworksSerializer(data=networks_data)
                network_serializer.create_network(data=networks_data)

            login(request, user)
            res = Response(
                {
                    "message": "User Authenticated, setting credentials",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                status=status.HTTP_201_CREATED,
            )
            res = set_authentication_cookies(res, access_token, refresh_token, request)

            logger.info("%s successful signed up", user.email)
            return res
        else:
            logger.warning("python social auth unable to authenticate user")
            return Response(
                {"error": "User Not Found By OAuth Code"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    except Exception as e:
        logger.error(f"Uncaught Exception Error: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([AllowAny])
@psa()
def login_by_access_token(request, backend) -> Response:
    code = request.data.get("code")
    if not code:
        logger.warning("Request does not have OAuth code")
        return Response(
            {"error": "No OAuth code provided."}, status=status.HTTP_401_UNAUTHORIZED
        )
    try:
        token_url = "https://www.googleapis.com/oauth2/v4/token"
        data = {
            "code": code,
            "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            "redirect_uri": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = requests.post(token_url, data=data)

        if response.status_code != 200:
            return Response(
                {"error": "Failed to get tokens from Google."},
                status=response.status_code,
            )

        tokens = response.json()
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
        user = request.backend.do_auth(access_token)

        if user:
            user_data = {
                "user_name": user.email,
                "user_email": user.email,
            }

            user_serializer = UserSerializer(data=user_data)
            existing_user = user_serializer.get_user_by_email(  # type:ignore
                data=user_data
            )
            if existing_user is None:
                res = Response(
                    {"message": "Login Failed. User Does Not Exist. Please Sign Up."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
                logger.warning(
                    "%s attempted to login, but does not yet have an account",
                    user.email,
                )
                return res

            login(request, user)

            res = Response(
                {
                    "message": "User Is Authenticated, Logging In...",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                status=status.HTTP_200_OK,
            )
            res = set_authentication_cookies(res, access_token, refresh_token, request)

            logger.info("%s is successfully authenticated, logging in...", user.email)
            return res
        else:
            logger.warning("python social auth unable to find user")
            return Response(
                {"message": "User Not Found in Database"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    except Exception as e:
        logger.error("%s Uncaught Exception Error:", str(e))
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@csrf_protect
@psa()
def authentication_test(request, backend) -> Response:
    try:
        access_token = request.COOKIES.get("access_token")
        if isinstance(request.user, User):
            AccessToken(access_token)
            return Response(
                {
                    "message": "Authorized: User successfully authenticated using Email/JWT Auth"
                },
                status=status.HTTP_200_OK,
            )
        elif request.backend.do_auth(access_token):
            return Response(
                {
                    "message": "Authorized: User successfully authenticated using Google OAuth2"
                },
                status=status.HTTP_200_OK,
            )
        elif isinstance(request.user, AnonymousUser):
            logger.warning("User Attempted To Login As AnonymousUser")
            return Response(
                {"message": "Unauthorized: Anonymous User Login Detected"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            logger.warning(
                "User %s failed all other authentiction checks", request.user
            )
            return Response(
                {
                    "message": "Unauthorized: User failed all other authentication checks"
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
    except Exception as e:
        logger.error("%s Uncaught Exception Error:", str(e))
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def check_token_hash(request) -> Response:
    try:
        token_str = request.data.get("token")
        email = redis_instance.get(f"signup_token_for_{token_str}")
        if not email:
            logger.error(f"Token not found or expired: {token_str}")
            return Response(
                {"message": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            return Response(
                {"message": "Token is Validated"}, status=status.HTTP_200_OK
            )
    except Exception as e:
        logger.error("%s Uncaught Exception Error:", str(e))
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def activate(request) -> Response:
    try:
        user_name = request.data.get("username")
        password = request.data.get("password")
        token_str = request.data.get("token")

        if not user_name or not password or not token_str:
            return Response(
                {"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST
            )

        logger.info(f"Received token: {token_str}")

        # Validates the username and password
        # against regex patterns (see auth_utils.py)
        if not user_name_pattern.match(user_name):
            return Response(
                {"message": "Invalid username"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not password_pattern.match(password):
            return Response(
                {"message": "Invalid password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Retrieve the email associated with the token from Redis
        email = redis_instance.get(f"signup_token_for_{token_str}")
        if not email:
            logger.error(f"Token not found or expired: {token_str}")
            return Response(
                {"message": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # NOTE: Decodes email data received from redis as utf-8 string
        email = email.decode("utf-8")
        logger.info(f"Token matched email: {email}")

        encrypted_password = encrypt(password, settings.SECRET_KEY)

        user_data = {
            "user_name": user_name,
            "user_password": encrypted_password,
            "user_email": email,
            "is_active": True,
        }

        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user_serializer.save()
            user = user_serializer.instance  # Get created user
        else:
            return Response(
                {"message": "User Credentials are not Valid via activate serializer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        redis_instance.delete(f"signup_token_for_{token_str}")

        # Generate Tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        res = Response(
            {
                "message": "User Authenticated, setting credentials",
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            status=status.HTTP_200_OK,
        )

        res = set_authentication_cookies(res, access_token, refresh_token, request)
        login(request, user, backend="users.auth.CookieTokenAuthentication")
        return res

    except Exception as e:
        logger.error(f"Unexpected error during account activation via email: {str(e)}")
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def email_registration_view(request) -> Response:
    try:
        logger.info("Received email registration request")
        serializer = EmailRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            logger.info(f"Valid email received: {email}")

            # Token generation
            token = generate_sha256_hash(email)
            logger.info(f"Generated token for email: {token}")

            # Store token in Redis
            redis_instance.set(
                f"signup_token_for_{token}", email, ex=600
            )  # Increased expiration time
            logger.info(f"Stored token in Redis for email: {email} with token: {token}")

            # Activation link containing the token
            activation_link = f"http://localhost:5173/onboarding/?token={token}"
            logger.info(f"Generated activation link: {activation_link}")

            # Email message with the activation link
            message = f"""
            <html>
            <body>
                <p>Thanks For Signing Up for Phlint! Please click on the button below to complete your sign up process!</p>
                <a href="{activation_link}" style="padding: 10px 20px; color: white; background-color: blue; text-decoration: none; border-radius: 5px;">Complete Sign Up</a>
            </body>
            </html>
            """

            # Log the email message for debugging purposes
            logger.info(f"Sending email to: {email} with message: {message}")

            # Send the activation email
            send_mail(
                "Email verification",
                "Text version.",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=message,
            )
            logger.info(f"Activation email sent to: {email}")

            return Response({"message": "Email sent!"}, status=status.HTTP_200_OK)
        else:
            logger.error(f"Email serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Uncaught Exception Error during email registration: {str(e)}")
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
