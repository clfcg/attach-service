from .views import index
from django.urls import path

app_name = 'attach'

urlpatterns = [
    path('', index, name='index')
]