from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ifscApi.getDetails import FetchData
import requests

# Assign IFSC code
ifsc = 'KKBK0005652'


def bank_details(ifsc):
    try:
        res = requests.get("https://ifsc.razorpay.com/" + ifsc)
        return res.json()
    except Exception as e:
        return Response({'error': e}, status=200)
