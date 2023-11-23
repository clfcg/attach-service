from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register('attach', views.HistlpuViewSet)

app_name = 'attach'

urlpatterns = [
    #path('shop_category/', views.ShopCategoryListView.as_view(), name='shop_category_list'), 
    #path('shop_category/<pk>/', views.ShopCategoryDetailView.as_view(), name='shop_category_detail'),
    path('', include(router.urls)),]