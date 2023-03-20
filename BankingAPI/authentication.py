from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime
from jwt import decode, InvalidTokenError
from django.conf import settings
import requests
import jwt
from rest_framework.response import Response
import json

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            auth_header = request.headers.get('Authorization')

            if not auth_header:
                raise AuthenticationFailed('Authorization header is missing')

            response = requests.get(settings.USERS_MICROSERVICE_LINK,
                                        headers = { 'Authorization': auth_header }
                                    )

            if response.ok :
                user = json.loads(response.json())
                return (user, None)

            error = json.loads(response.json())
            return (None, {"status_code" : response.status_code, "error" : error})

        except Exception as e:
            return (None, str(e))

