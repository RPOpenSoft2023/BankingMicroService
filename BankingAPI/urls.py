from django.urls import path
from .views import *

urlpatterns = [
    path('accounts/', accounts),
    path('transactions/', transactions),
    path('create_account/', create_account),
    path('delete_account/', delete_account),
    path('add_transactions/', add_transactions),
]