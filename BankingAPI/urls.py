from django.urls import path
from .views import *

urlpatterns = [
    path('accounts/', account),
    path('transactions/', transactions),

]