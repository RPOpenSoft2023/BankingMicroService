from django.urls import path
from .views import *

urlpatterns = [
    path('accounts/', accounts),
    path('transactions/', transactions),
    path('create_account/', create_account),
    path('delete_account/', delete_account),
    path('add_transactions/', add_transactions),
    path('add_transaction/', add_transaction),
    path('edit_transaction/', edit_transaction),
    path('update_account/', update_account),
    path('get_transaction/', get_transaction),
    path('get_categories/', get_categories)
]
