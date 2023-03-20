from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from .authentication import CustomAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import PageNumberPagination
from .serializers import AccountSerializer
from .serializers import TransactionSerializer
from .models import Account
from .models import Transaction
from django.conf import settings

@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def accounts(request):
    try:   
        user = request.user
        if (user == None):
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if 'account_number' in request.GET:    
            account_number = request.GET['account_number']           
            account = Account.objects.get(account_number = account_number)
            serializer = AccountSerializer(account)
            return Response(serializer.data)
        
        phone_number = user['phone']
        accounts = Account.objects.all().filter(phone_number = phone_number)
        paginator = PageNumberPagination()
        paginator.page_size = settings.PAGE_SIZE
        if 'page_size' in request.GET:
            paginator.page_size = request.GET['page_size']
        result_page = paginator.paginate_queryset(accounts, request)
        serializer = AccountSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    



@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def transactions(request):
    try:
       
        user = request.user
        print(user)
        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        phone_number = user['phone']

        accounts = Account.objects.filter(phone_number = phone_number)

        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        print(start_date)
        if 'account_number' in request.GET:    
            account_number = request.GET['account_number']
            account = Account.objects.get(pk = account_number)
            if account not in accounts:
                return Response({'error': 'You are trying to access of an account which is not yours'},status = 401)
             
            paginator = PageNumberPagination()
            paginator.page_size = settings.PAGE_SIZE
            if 'page_size' in request.GET:
              paginator.page_size = request.GET['page_size']
            transactions = Transaction.objects.filter(account = account).filter(date__gte=start_date).filter(date__lte=end_date)
            transactions = paginator.paginate_queryset(transactions, request)
            serializer = TransactionSerializer(transactions, many = True)
            return paginator.get_paginated_response(serializer.data)

        paginator = PageNumberPagination()
        paginator.page_size = settings.PAGE_SIZE
        if 'page_size' in request.GET:
            paginator.page_size = request.GET['page_size']
        print(paginator.page_size)    
        list_transaction = Transaction.objects.filter(account__in=accounts).filter(date__gte=start_date).filter(date__lte=end_date)
        print(list_transaction)
        transactions = paginator.paginate_queryset(list_transaction, request)
        
        serializer = TransactionSerializer(transactions, many=True)
        
        return paginator.get_paginated_response(serializer.data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)

