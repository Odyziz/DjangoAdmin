from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.montaze, name="montaze"),
    path('id/<id>', views.montaz, name="montaz"),
    path('archiwum', views.archiwum, name="archiwum"),
    path('wyslij_sms_montaz', views.wyslij_sms_montaz, name="wyslij_sms_montaz"),
] 

