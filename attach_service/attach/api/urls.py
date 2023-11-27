from django.urls import path, include
from rest_framework import routers
from . import views


#router = routers.DefaultRouter()
#router.register('attach', views.HistlpuViewSet)

app_name = 'attach'

urlpatterns = [
    path('GetViewDataAttachStart/', views.GetViewDataAttachStartView.as_view(), name="attach_view_start"),
    #path('shop_category/', views.ShopCategoryListView.as_view(), name='shop_category_list'), 
    #path('shop_category/<pk>/', views.ShopCategoryDetailView.as_view(), name='shop_category_detail'),
    #path('', include(router.urls)),
    ]

#curl -X POST http://127.0.0.1:5000/api/GetViewDataAttachStart/ -d '{"id_request": "kek", "date_q": "2023-11-01"}' -H 'Content-Type: application/json'