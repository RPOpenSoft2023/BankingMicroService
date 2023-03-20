from django.urls import path
from .views import *

urlpatterns = [
    path('accounts/', accounts),
    path('transactions/', transactions),

]