from django.conf import settings
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.exceptions import AuthenticationFailed

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, authentication_classes

import pandas as pd
from twilio.rest import Client

from .authentication import CustomAuthentication
from .serializers import AccountSerializer, TransactionSerializer
from .models import Account as AccountModel, Transaction as TransactionModel


@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def accounts(request):
    try:
        user = request.user
        if (user == None):
            return Response({'error': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)

        phone_number = user['phone']
        accounts = AccountModel.objects.all().filter(phone_number=phone_number)

        if 'account_number' in request.GET:
            account_number = request.GET['account_number']
            account = AccountModel.objects.get(account_number=account_number)

            if account not in accounts:
                return Response(
                    {
                        "error":
                        'You are trying to access an account which is not yours'
                    },
                    status=401)

            serializer = AccountSerializer(account)
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

        if user is None:
            return Response({'error': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)

        phone_number = user['phone']
        accounts = AccountModel.objects.filter(phone_number=phone_number)
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']

        paginator = PageNumberPagination()
        paginator.page_size = settings.PAGE_SIZE
        if 'page_size' in request.GET:
            paginator.page_size = request.GET['page_size']

        if 'account_number' in request.GET:
            account_number = request.GET['account_number']
            account = AccountModel.objects.get(pk=account_number)

            if account not in accounts:
                return Response(
                    {
                        'error':
                        'You are trying to access an account which is not yours'
                    },
                    status=401)

            transactions = TransactionModel.objects.filter(
                account=account).filter(date__gte=start_date).filter(
                    date__lte=end_date)
        else:
            transactions = TransactionModel.objects.filter(
                account__in=accounts).filter(date__gte=start_date).filter(
                    date__lte=end_date)

        page = paginator.paginate_queryset(transactions, request)
        serializer = TransactionSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def create_account(request):
    try:
        user = request.user

        if user is None:
            return Response({'error': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)

        data = {}
        data['account_number'] = request.data["account_number"]
        try:
            account_exists = AccountModel.objects.get(
                pk=data['account_number'])
            return Response(
                {
                    'error':
                    'an account with that account number already exists'
                },
                status=400)
        except:
            pass

        data['ifsc'] = request.data["ifsc_code"]
        data['branch_name'] = request.data["branch_name"]
        data['account_opening_date'] = request.data["account_opening_date"]
        data['account_type'] = request.data["account_type"]
        data['bank_name'] = request.data["bank_name"]
        data['branch_address'] = request.data["branch_address"]
        data['phone_number'] = user["phone"]

        new_account = AccountSerializer(data=data)
        new_account.is_valid(raise_exception=True)
        new_account.save()

        account_sid = settings.ACCOUNTS_SID
        auth_token = settings.AUTH_TOKEN
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="Congratulations! Account created successfully.",
            from_=settings.PHONE,
            to="+91" + data['phone_number'])

        return Response({'message': 'account created successfully'})

    except Exception as e:
        return Response({'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@authentication_classes([CustomAuthentication])
def delete_account(request):
    try:
        user = request.user

        if user is None:
            return Response({'error': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)

        account_number = request.data["account_number"]
        account = AccountModel.objects.get(account_number)

        if (account is None):
            return Response(
                {
                    'error':
                    'account with that account number does not exists, nothing to delete'
                },
                status=400)

        if account.phone_number != user['phone']:
            return Response(
                {
                    'error':
                    'You are trying to access an account which is not yours'
                },
                status=401)

        AccountModel.objects.remove(account_number)
        return Response({"message": "account deleted successfully"},
                        status=200)

    except Exception as e:
        return Response({'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@authentication_classes([CustomAuthentication])
def add_transactions(request, format=None):
    try:
        user = request.user

        if user is None:
            return Response({'error': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)

        account_number = request.data["account_number"]
        account = AccountModel.objects.get(pk=account_number)

        transactions_file = request.FILES.get('transactions')
        df = pd.read_csv(transactions_file)

        for row in df.iterrows():
            transaction = TransactionSerializer(
                account=account,
                Date=row['Date'],
                description=row['description'],
                Debit=row['Debit'],
                Credit=row['Credit'],
                Balance=row['Balance'],
            )
            print(transaction)
            # transaction.save()
        return Response({'message': 'Transactions updated'})

    except Exception as e:
        return Response({'message': f'Error: {str(e)}'})
