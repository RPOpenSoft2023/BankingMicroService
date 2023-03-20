import os
from twilio.rest import Client
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.conf import settings
import jwt
import datetime
from django.contrib.auth import authenticate
from rest_framework import status
from . import models, serializers
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from .models import Account
from .models import Transaction

# Create your views here.
@api_view(['POST'])
@authentication_classes({TokenAuthentication})
def create_account(request):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'message': 'Authorization header is missing'}, status=status.HTTP_401_UNAUTHORIZED)
        _, token = auth_header.split()
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        
        user_exists = models.User.objects.get(decoded_token.get('phone'))
        if(user_exists is not None) :
            return Response({'message':'an account with that phone number already exists'},status=400)
        
        account_number = request.data["account_number"]
        account_exists = models.Account.objects.get("account_number")
        if(account_exists is not None) :
            return Response({'message':'an account with that account number already exists'},status=400)
        password = request.data["password"]
        ifsc = request.data["ifsc_code"]
        account_opening_date = request.data["account_opening_date"]
        account_type = request.data["account_type"]
        bank_name = request.data["bank_name"]
        branch_address = request.data["branch_address"]
        branch_name = request.data["branch_name"]
        ph_No = request.data["phone"]

        new_account = serializers.AccountSerializer(request)
        new_account.save()

        # account_sid = "AC031bd3d4e1958d1a580cbf9ddce40b90"
        account_sid = settings.ACCOUNTS_SID
        # auth_token = "8766fe4f0d4cd538a329e60ed2c1a8fe"
        auth_token = settings.AUTH_TOKEN
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        body="Congratulations! Account created successfully.",
        from_=settings.PHONE,
        to="+91" + ph_No
        )
        print(message.sid)

        return Response({'message':'account created successfully'})
    
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes({TokenAuthentication})
def delete_account(request):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'message': 'Authorization header is missing'}, status=status.HTTP_401_UNAUTHORIZED)
        _, token = auth_header.split()
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        user_exists = models.User.objects.get(decoded_token.get('phone'))
        if(user_exists is not None) :
            return Response({'message':'an account with that phone number already exists'},status=400)
        
        account_number = request.data["account_number"]
        account_exists = models.Account.objects.get("account_number")
        if(account_exists is None) :
            return Response({'message':'account with that account number does not exists, nothing to delete'},status=400)
        models.Account.objects.remove(account_number)

        ph_No = request.data["phone"]
        # account_sid = "AC031bd3d4e1958d1a580cbf9ddce40b90"
        account_sid = settings.ACCOUNTS_SID
        # auth_token = "8766fe4f0d4cd538a329e60ed2c1a8fe"
        auth_token = settings.AUTH_TOKEN
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        body="Account deleted successfully.",
        from_=settings.PHONE,
        to="+91" + ph_No
        )
        print(message.sid)
        
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)