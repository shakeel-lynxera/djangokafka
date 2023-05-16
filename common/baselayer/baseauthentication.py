import jwt

from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import csrf_exempt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from common.baselayer.basemodel import StatusChoices
from cryptography.fernet import Fernet
from djangokafka.settings import (
    USERMS_FERTNET_SECRET_KEY,
    USERMS_JWT_ENCODING_SECRET_KEY,
)


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class UserAuthentication(BaseAuthentication):
    """
    custom authentication class for DRF, Fernet and JWT
    """

    @csrf_exempt
    def authenticate(self, request):
        print(f"Request Path: {request.path}")

        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            raise exceptions.AuthenticationFailed("User token is required")

        try:
            """DECODE FERNET TOKEN"""
            access_token = authorization_header.split(" ")[1]

            """VERIFY TOKEN IN BLACKLIST"""

            access_token = (
                Fernet(USERMS_FERTNET_SECRET_KEY)
                .decrypt(access_token.encode())
                .decode()
            )
        except IndexError:
            raise exceptions.AuthenticationFailed("Token prefix missing")
        except Exception as fernet_exception:
            print(f"Fernet exception:- {fernet_exception}")
            raise exceptions.AuthenticationFailed("Invalid token")

        try:
            payload = jwt.decode(
                access_token, USERMS_JWT_ENCODING_SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise exceptions.NotAcceptable("Invalid token")

        """VERIFY USER IN USER MODEL FROM DECODED PAYLOAD"""

        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        return user, None
