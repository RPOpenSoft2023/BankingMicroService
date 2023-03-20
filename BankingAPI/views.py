from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import PageNumberPagination
import jwt
from .serializers import AccountSerializer
from .serializers import TransactionSerializer
from .models import Account
from .models import Transaction

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def list_accounts(request):
    try:
        if not request.auth:
            raise AuthenticationFailed('Invalid or missing access token')
        
        paginator = PageNumberPagination()
        accounts = paginator.paginate_queryset(Account.objects.all(), request)
        
        serializer = AccountSerializer(accounts, many=True)
        
        response = {
            'listaccounts': serializer.data,
        }
        return paginator.get_paginated_response(response)
        
    except Exception as e:
        return Response({'error': 'An error occurred'}, status=500)
    


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def account(request):
    try:
        if not request.auth:
            raise AuthenticationFailed('Invalid or missing access token')

        account_number = request.get('account_number')
        account = Account.objects.all.values(account_number = account_number)
        serializer = AccountSerializer(account)
        
        response = serializer.data
        return response
        
    except Exception as e:
        return Response({'error': 'An error occurred'}, status=500)
    



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def transactions(request):
    try:
        if not request.auth:
            raise AuthenticationFailed('Invalid or missing access token')
        
        start_date = request.get('start_date')
        end_date = request.get('end_date')
        paginator = PageNumberPagination()
        list_transaction = Transaction.objects.all()
        valid_transactions = []
        for current_transaction in list_transaction:
            if(current_transaction.Date > start_date and current_transaction.Date < end_date):
                valid_transactions.append(current_transaction)
        transactions = paginator.paginate_queryset(valid_transactions, request)
        
        serializer = TransactionSerializer(transactions, many=True)
        
        response = {
            'transactions': serializer.data,
        }
        return paginator.get_paginated_response(response)
        
    except Exception as e:
        return Response({'error': 'An error occurred'}, status=500)
    



