from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime
from jwt import decode, InvalidTokenError
from django.conf import settings
import requests
import jwt
from rest_framework.response import Response
import json

get_user_api = ""

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed('Authorization header is missing')
        
        auth_token = auth_header.split(' ')[1]
        
        response = requests.get('http://localhost:8000/users/api/verify_token/',
                            headers = {
                                'Authorization': f'Bearer {auth_token}'
                            }
                        )
        #user_response = user.decode(auth_token, settings.SECRET_KEY, algorithms = ['HS256'])
        if response.ok :
            return (json.loads(response.json()),None)
        return (None,{"status_code" : response.status_code, "error":json.loads(response.json())})
    

