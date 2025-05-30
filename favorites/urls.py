from django.urls import path
from . import views

app_name = 'favorites'


urlpatterns = [
    path('fav_list/', views.fav_list, name='fav_list'),
    path('api/change/<int:ad_id>', views.fav_change, name='change'),
    path('remove/<int:ad_id>/', views.remove_fav, name='remove_fav'),
]