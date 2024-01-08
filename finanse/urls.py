from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.finanse, name="finanse"),
    path('wystaw_faktury', views.wystaw_faktury, name="wystaw_faktury"),
    path('ksiegowanie', views.ksiegowanie, name="ksiegowanie"),
    path('wyslij_maile', views.wyslij_maile, name="wyslij_maile"),
] 

