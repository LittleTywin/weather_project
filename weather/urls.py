from django.contrib import admin
from django.urls import path, re_path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('new_location<int:station_id>/', views.new_location, name='new_location'),
    path('delete_location<int:station_id>/', views.delete_location, name='delete_location'),
    path('set_default<int:station_id>/', views.set_default, name='set_default'),
    #re_path('.', views.url_not_found)
]
