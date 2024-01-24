from .views import index, api_log
from django.urls import path

app_name = 'attach'

urlpatterns = [
    path('', index, name='index'),
    path('logs/', api_log, name='log')
]