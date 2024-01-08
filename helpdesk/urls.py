from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.zgloszenia, name="zgloszenia"),
    path('id/<id>', views.zgloszenie, name="zgloszenie"),
    
] 
