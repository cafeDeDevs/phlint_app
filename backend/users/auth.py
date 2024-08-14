from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from users.models import User
from users.utils.auth_utils import *


class CookieTokenAuthentication(BaseAuthentication):
    # TODO: Add more logic regarding refresh_token
    def authenticate(self, request):
        access_token = request.COOKIES.get("access_token")
        #  refresh_token = request.COOKIES.get("refresh_token")
        if not access_token:
            return None

        try:
            if access_token.count(".") == 2:
                payload = AccessToken(access_token).payload
                user_id = payload.get("user_id")
                user = self.get_user(user_id)
                if user:
                    return (user, access_token)
            else:
                return None
        except Exception as e:
            logger.error("Authentication error: %s", str(e))
            raise AuthenticationFailed("Invalid token")

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except Exception as e:
            logger.error("Error getting User by id: %s", str(e))
            return None
