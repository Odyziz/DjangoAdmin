from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.klienci, name="klienci"),
    path('id/<id>', views.klient, name="klient"),
    path('wyslij_mail', views.wyslij_mail, name="wyslij_mail"),
    path('wyslij_sms', views.wyslij_sms, name="wyslij_sms"),
    path('dodaj_skan', views.dodaj_skan, name="dodaj_skan"),
    path('wystaw_fakture', views.wystaw_fakture, name="wystaw_fakture"),
    path('wyslij_fakture/<id>', views.wyslij_fakture, name="wyslij_fakture"),
    path('umowa_podpisana/<id>', views.umowa_podpisana, name="umowa_podpisana"),
    path('umowa_wyslij/<id>', views.umowa_wyslij, name="umowa_wyslij"),
    path('dodaj_wplate', views.dodaj_wplate, name="dodaj_wplate"),
    path('generuj_raportCSV', views.generuj_raportCSV, name="generuj_raportCSV"),
    path('generuj_umowe', views.generuj_umowe, name="generuj_umowe"),
    path('profil_klienta', views.profil_klienta, name="profil_klienta"),
] 

