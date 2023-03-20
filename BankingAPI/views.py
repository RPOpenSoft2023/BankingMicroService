from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from .authentication import CustomAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import PageNumberPagination
import jwt
from .serializers import AccountSerializer
from .serializers import TransactionSerializer
from .models import Account
from .models import Transaction

from twilio.rest import Client

@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def accounts(request):
    try:   

        user = request.user

        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        

        account_number = request.get('account_number')
        phone_number = request.get('phone_number')

        if account_number is not None:               
            account = Account.objects.get(account_number = account_number)
            serializer = AccountSerializer(account)
            return serializer.data


        paginator = PageNumberPagination()
        accounts = paginator.paginate_queryset(Account.objects.all().filter(phone_number = phone_number), request)
        
        serializer = AccountSerializer(accounts, many=True)
        
        response = {
            'accounts': serializer.data,
        }
        return paginator.get_paginated_response(response)
        
    except Exception as e:
        return Response({'error': 'An error occurred'}, status=500)
    



@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def transactions(request):
    try:
       
        user = request.user

        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        account_number = request.get('account_number')

        start_date = request.get('start_date')
        end_date = request.get('end_date')

        if account_number is not None:               
            paginator = PageNumberPagination()
            transactions = Transaction.objects.filter(account = account_number).filter(Date = [start_date, end_date])
            transactions = paginator.paginate_queryset(transactions, request)
            serializer = TransactionSerializer(transactions, many = True)
            response = {
                       'transactions': serializer.data,
                   }
            return paginator.get_paginated_response(response)

        paginator = PageNumberPagination()
        list_transaction = Transaction.objects.all().filter(Date = [start_date, end_date])
        transactions = paginator.paginate_queryset(list_transaction, request)
        
        serializer = TransactionSerializer(transactions, many=True)
        
        response = {
            'transactions': serializer.data,
        }
        return paginator.get_paginated_response(response)
        
    except Exception as e:
        return Response({'error': 'An error occurred'}, status=500)

    
    
@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def create_account(request):
    try:
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
@authentication_classes([CustomAuthentication])
def delete_account(request):
    try:
        account_number = request.data["account_number"]
        account_exists = models.Account.objects.get("account_number")
        if(account_exists is None) :
            return Response({'message':'account with that account number does not exists, nothing to delete'},status=400)
        models.Account.objects.remove(account_number)

        # ph_No = request.data["phone"]
        # # account_sid = "AC031bd3d4e1958d1a580cbf9ddce40b90"
        # account_sid = settings.ACCOUNTS_SID
        # # auth_token = "8766fe4f0d4cd538a329e60ed2c1a8fe"
        # auth_token = settings.AUTH_TOKEN
        # client = Client(account_sid, auth_token)
        # message = client.messages.create(
        # body="Account deleted successfully.",
        # from_=settings.PHONE,
        # to="+91" + ph_No
        # )
        # print(message.sid)
        
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
