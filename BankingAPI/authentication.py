from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime
import jwt
from jwt import decode, InvalidTokenError
from django.conf import settings
import requests
from rest_framework.response import Response
import json
from rest_framework.views import exception_handler

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
                user = response.json()
                # print(user)
                return (user, None)
            error = response.json()
            raise AuthenticationFailed({"status":response.status_code, "error" : error})

        except Exception as e:
            raise AuthenticationFailed({"status":response.status_code, "error":str(e)})

