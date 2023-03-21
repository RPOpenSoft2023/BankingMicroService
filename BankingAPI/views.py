from django.conf import settings

from rest_framework.response import Response

from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, authentication_classes

import pandas as pd
from twilio.rest import Client

from .authentication import CustomAuthentication
from .serializers import AccountSerializer, TransactionSerializer
from .models import Account, Transaction 
from .utils import *


TRANSACTION_COLS = ['Date', 'Particulars', 'Debit','Credit', 'Balance']

@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def accounts(request):
    try:
        user = request.user

        phone_number = user['phone']
        accounts = Account.objects.all().filter(phone_number=phone_number)

        if 'account_number' in request.GET:
            account_number = request.GET['account_number']
            account = Account.objects.get(account_number=account_number)

            if account not in accounts:
                return Response({"error":'You are trying to access an account which is not yours'}, status=401)
            serializer = AccountSerializer(account)
            return Response(serializer.data, status=200)
        
        else:
            paginator = PageNumberPagination()
            paginator.page_size = settings.PAGE_SIZE
            if 'page_size' in request.GET:
                paginator.page_size = request.GET['page_size']

            page = paginator.paginate_queryset(accounts, request)
            serializer = AccountSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def transactions(request):
    try:
        user = request.user
        phone_number = user['phone']

        accounts = Account.objects.filter(phone_number=phone_number)
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']

        paginator = PageNumberPagination()
        paginator.page_size = settings.PAGE_SIZE
        if 'page_size' in request.GET:
            paginator.page_size = request.GET['page_size']

        if 'account_number' in request.GET:
            account_number = request.GET['account_number']
            account = Account.objects.get(pk=account_number)
            print(account)

            if account not in accounts:
                return Response({'error':'You are trying to access an account which is not yours'}, status=401)

            transactions = Transaction.objects.filter(
                account=account).filter(date__gte=start_date).filter(
                    date__lte=end_date)
            print(transactions)
        else:
            transactions = Transaction.objects.filter(
                account__in=accounts).filter(date__gte=start_date).filter(
                    date__lte=end_date)

        page = paginator.paginate_queryset(transactions, request)
        serializer = TransactionSerializer(page, many=True)
        print(serializer.data)
        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def create_account(request):
    try:
        user = request.user
        
        if Account.objects.filter(account_number=request.data['account_number']).first():
            return Response({"error":"Account already exists"}, status=400)

        branch_details = bank_details(request.data["ifsc"])
        if branch_details == "Not Found":
            return Response({"error":"Invalid IFSC code"}, status=404)

        if int(request.data["phone_number"]) != int(user['phone']):
            return Response({'error': "User's phone number doesn't match with the one provided. "}, status=401)

        account = AccountSerializer(data=request.data)
        account.is_valid(raise_exception=True)
        account.save()

        return Response({
            'message': 'Account created successfully',
            'account': account.data
            }, status=200)

    except Exception as e:
        return Response({'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@authentication_classes([CustomAuthentication])
def delete_account(request):
    try:
        user = request.user
        # print(user)
        account_number = request.data["account_number"]
        account = Account.objects.get(account_number=account_number)
        print(account)
        if int(account.phone_number) != int(user['phone']):
            return Response({'error':'You are trying to access an account which is not yours'}, status=401)

        account.delete()
        return Response({"message": "Account deleted successfully"}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@authentication_classes([CustomAuthentication])
def add_transactions(request):
    try:
        user = request.user

        account_number = request.data["account_number"]
        account = Account.objects.get(pk=account_number)

        if int(account.phone_number) != int(user['phone']):
            return Response({'error': 'You are trying to add transactions for an account which is not yours'}, status=401)

        transactions_file = request.FILES.get('transactions')
        df = pd.read_csv(transactions_file, usecols=TRANSACTION_COLS)
        df = df.dropna(subset=['Date'])
        df = df.reset_index()
        df = df.fillna(value=0)

        for i in range(len(df)):
            data={
                "account":str(account),
                "date":df.loc[i,'Date'],
                "description":df.loc[i,'Particulars'],
                "debit":df.loc[i,'Debit'].astype('int'),
                "credit":df.loc[i,'Credit'].astype('int'),
                "balance":df.loc[i,'Balance'].astype('int'),
            }
            transaction = TransactionSerializer(data=data)
            if transaction.is_valid(raise_exception=True):
                transaction.save()

        return Response({'message': 'Transactions updated successfully'}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=500)
