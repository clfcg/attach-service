from django.urls import path, include
from . import views


app_name = 'attach'

urlpatterns = [
    path('GetViewDataAttachStart/', views.GetViewDataAttachStartView().as_view(), name="attach_view_start"),
    path('GetViewDataAttachPoll/', views.GetViewDataAttachPollView().as_view(), name="attach_view_poll"),
    path('GetPersonaData/', views.GetPersonaDataView().as_view(), name='persona_data'),
    path('GetNewAttachByPeriod/', views.GetNewAttachByPeriod().as_view(), name='new_attach_by_period'),
    path('GetAttachStatusChange/', views.GetAttachStatusChangeView().as_view(), name='attach_change'),
    #path('shop_category/', views.ShopCategoryListView.as_view(), name='shop_category_list'), 
    #path('shop_category/<pk>/', views.ShopCategoryDetailView.as_view(), name='shop_category_detail'),
    #path('', include(router.urls)),
    ]