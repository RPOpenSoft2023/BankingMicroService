from django.urls import path
from .views import *

urlpatterns = [
    path('list_accounts/', list_accounts),
    path('account/', account),
    path('transactions/', transactions),

]