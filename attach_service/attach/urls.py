from .views import index, api_logs_table_view, api_log
from django.urls import path

app_name = 'attach'

urlpatterns = [
    path('', index, name='index'),
#    path('logs/', api_log, name='logs'),
    path('api_logs/', api_logs_table_view, name='api_logs'),
    path('api_search/', api_log, name='api_search')
]