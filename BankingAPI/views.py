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

