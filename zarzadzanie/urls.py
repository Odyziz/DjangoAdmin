from django.urls import path, include
from . import views
# Create your views here.

urlpatterns = [
    path('', views.zarzadzanie, name="zarzadzanie"),
    path('spisAdresow/', views.spisAdresow, name="spisAdresow"),
    path('dodajAdres/', views.dodajAdres, name="dodajAdres"),
    path('rejestracja/', views.rejestracja, name="rejestracja"),
    path('spisNumerow/', views.spisNumerow, name="spisNumerow"), 
    path('spisTaryf/', views.spisTaryf, name="spisTaryf"), 
    path('spisTaryf/id/<id>', views.taryfaSzczegoly, name="taryfaSzczegoly"),
    path('generuj_raport/', views.generuj_raport, name="generuj_raport"), 
    path('spisPakietow/', views.spisPakietow, name="spisPakietow"),
    path('spisPakietow/id/<id>', views.pakietSzczegoly, name="pakietSzczegoly"), 
    path('spisUzytkownikow/', views.spisUzytkownikow, name="spisUzytkownikow"),
    path('spisUzytkownikow/grupa/<nazwa>', views.uzytkownicy, name="uzytkownicy"),
]
