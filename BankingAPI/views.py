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

TRANSACTION_COLS = [
    'Date', 'Particulars', 'Debit', 'Credit', 'Balance', 'Category'
]


@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def accounts(request):
    try:
        user = request.user

        phone_number = user['phone_number']
        accounts = Account.objects.all().filter(phone_number=phone_number)

        if 'account_number' in request.GET:
            account_number = request.GET['account_number']
            account = Account.objects.get(account_number=account_number)

            if account not in accounts:
                return Response(
                    {
                        "error":
                        'You are trying to access an account which is not yours'
                    },
                    status=401)
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
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def transactions(request):
    try:
        user = request.user
        phone_number = user['phone_number']

        accounts = Account.objects.filter(phone_number=phone_number)

        paginator = PageNumberPagination()
        paginator.page_size = settings.PAGE_SIZE
        if 'page_size' in request.GET:
            paginator.page_size = request.GET['page_size']

        if 'account_number' in request.GET:
            account_number = request.GET['account_number']
            account = Account.objects.get(pk=account_number)

            if account not in accounts:
                return Response(
                    {
                        'error':
                        'You are trying to access an account which is not yours'
                    },
                    status=401)

            transactions = Transaction.objects.filter(account=account)
            if "start_date" in request.GET:
                transactions = transactions.filter(
                    date__gte=request.GET["start_date"])
            if "end_date" in request.GET:
                transactions = transactions.filter(
                    date__lte=request.GET["end_date"])
        else:
            transactions = Transaction.objects.filter(account__in=accounts)
            if "start_date" in request.GET:
                transactions = transactions.filter(
                    date__gte=request.GET["start_date"])
            if "end_date" in request.GET:
                transactions = transactions.filter(
                    date__lte=request.GET["end_date"])

        page = paginator.paginate_queryset(transactions, request)
        serializer = TransactionSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def create_account(request):
    try:
        user = request.user

        if Account.objects.filter(
                account_number=request.data['account_number']).first():
            return Response({"error": "Account already exists"}, status=400)

        branch_details = bank_details(request.data["ifsc"])
        if branch_details == "Not Found":
            return Response({"error": "Invalid IFSC code"}, status=404)

        account = AccountSerializer(
            data={
                **request.data, 'phone_number': user['phone_number']
            })
        account.is_valid(raise_exception=True)
        account.save()
        return Response(
            {
                'message': 'Account created successfully',
                'account': account.data
            },
            status=200)

    except Exception as e:
        return Response({'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@authentication_classes([CustomAuthentication])
def update_account(request):
    try:
        user = request.user

        account_number = str(request.data["account_number"])
        print(account_number)
        account = Account.objects.filter(account_number=account_number).first()

        if account is None:
            return Response({'error': 'No such account exists'}, status=400)

        if str(account.phone_number) != str(user['phone_number']):
            return Response(
                {
                    'error':
                    'You are trying to access an account which is not yours'
                },
                status=401)

        if "phone_number" in request.data:
            return Response(
                {"error": "You can't update phone number directly"},
                status=403)

        if "ifsc" in request.data:
            branch_details = bank_details(request.data["ifsc"])
            if branch_details == "Not Found":
                return Response({"error": "Invalid IFSC code"}, status=404)
            account.ifsc = request.data["ifsc"]

        if ("account_number" in request.data):
            print("Reached")
            if (len(account_number) < 11 or len(account_number) > 16):
                return Response({"error": "Invalid account number"},
                                status=400)

        for key in request.data:
            print(key)
            if key in ["ifsc", "phone_number"]: continue
            print(request.data[key])
            setattr(account, key, request.data[key])

        account.save()

        return Response({"message": "User data updated successfully"},
                        status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([CustomAuthentication])
def delete_account(request):
    try:
        user = request.user
        account_number = request.data["account_number"]
        account = Account.objects.get(account_number=account_number)
        print(account)

        if str(account.phone_number) != str(user['phone_number']):
            return Response(
                {
                    'error':
                    'You are trying to access an account which is not yours'
                },
                status=401)

        account.delete()
        return Response({"message": "Account deleted successfully"},
                        status=200)

    except Exception as e:
        return Response({'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@authentication_classes([CustomAuthentication])
def add_transactions(request):
    try:
        user = request.user

        account_number = request.data["account_number"]
        account = Account.objects.get(pk=account_number)

        if str(account.phone_number) != str(user['phone_number']):
            return Response(
                {
                    'error':
                    'You are trying to add transactions for an account which is not yours'
                },
                status=401)

        transactions_file = request.FILES.get('transactions')
        df = pd.read_csv(transactions_file, usecols=TRANSACTION_COLS)
        df = df.dropna(subset=['Date'])
        df = df.reset_index()
        df = df.fillna(value=0)

        for i in range(len(df)):
            data = {
                "account":
                str(account),
                "date":
                df.loc[i, 'Date'],
                "description":
                df.loc[i, 'Particulars'],
                "debit":
                df.loc[i, 'Debit'].astype('int'),
                "credit":
                df.loc[i, 'Credit'].astype('int'),
                "balance":
                df.loc[i, 'Balance'].astype('int'),
                "category":
                'others' if df.loc[i, 'Category'] == 0 else df.loc[i,
                                                                   'Category'],
            }
            transaction = TransactionSerializer(data=data)
            if transaction.is_valid(raise_exception=True):
                transaction.save()

        return Response({'message': 'Transactions updated successfully'},
                        status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(["PUT"])
@authentication_classes([CustomAuthentication])
def edit_transaction(request):
    try:
        user = request.user

        transaction_id = request.data["transaction_id"]
        transaction = Transaction.objects.get(pk=transaction_id)

        account = transaction.account

        if str(account.phone_number) != str(user['phone_number']):
            return Response(
                {
                    'error':
                    'You are trying to edit a transaction which does not belonng to your account'
                },
                status=401)

        new_category = str(request.data.get('new_category'))
        if new_category:
            account.category = new_category

        note = str(request.data.get('note'))
        if note:
            account.note = note

        transaction = TransactionSerializer(data={
            **request.data, 'account': account
        })
        transaction.is_valid(raise_exception=True)
        transaction.save()

        return Response({'message': 'transaction updated'}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['PUT'])
@authentication_classes([CustomAuthentication])
def add_transaction(request):
    try:
        user = request.user

        account_number = request.data['account_number']

        account = Account.objects.filter(account_number=account_number).first()

        if account is None:
            return Response({'error': 'No such account exists'}, status=400)

        if str(account.phone_number) != str(user['phone_number']):
            return Response(
                {
                    'error':
                    'You are trying to add transactions for an account which is not yours'
                },
                status=403)

        serializer = TransactionSerializer(data={
            **request.data, 'account': account
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success': 'Transaction added successfully'},
                        status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def get_transaction(request):
    try:
        user = request.user

        transaction_id = request.data['transaction_id']

        transaction = Transaction.objects.filter(id=transaction_id).first()

        if transaction is None:
            return Response({'error': 'No such account exists'}, status=400)

        if str(transaction.account.phone_number) != str(user['phone_number']):
            return Response(
                {
                    'error':
                    'You are trying to get transactions for an account which is not yours'
                },
                status=403)

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)
