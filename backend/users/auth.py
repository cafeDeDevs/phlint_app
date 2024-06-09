from django.conf import settings
from django.contrib.auth.models import User

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token


class CookieTokenAuthentication(BaseAuthentication):
    # TODO: Add more logic regarding refresh_token
    def authenticate(self, request):
        token_key = request.COOKIES.get('access_token')
        if not token_key:
            return None

        try:
            token = Token.objects.get(key=token_key)  # type: ignore
        except Token.DoesNotExist:  # type: ignore
            raise AuthenticationFailed('Invalid token')

        return (token.user, token)
