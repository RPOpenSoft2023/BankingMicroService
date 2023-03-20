from django.views import path
from .views import create_account
from .views import delete_account
  
urlpatterns = [
    path('create_account/', create_account ),
    path('delete_account/', delete_account ),
]