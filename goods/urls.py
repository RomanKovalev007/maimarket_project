from django.urls import path
from . import views

app_name = 'goods'


urlpatterns = [
    path('additem/', views.AddAd.as_view(), name='add_ad'),
    path('ad/<slug:ad_slug>/', views.show_ad, name='ad'),
    path('list/', views.goods_list, name='goods_list'),
    path('edit/<slug:ad_slug>/', views.edit_ad, name='edit'),
    path('publish/<slug:ad_slug>/', views.remove_ad, name='publish'),
]