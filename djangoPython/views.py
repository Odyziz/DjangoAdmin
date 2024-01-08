from itertools import count
from django.forms import models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from klienci.models import Klient, Faktura
from montaze.models import Montaz
from helpdesk.models import Zgloszenie


import datetime
from . import settings


@login_required(login_url="logowanie")
def glowna(request):
    zalogowany = User.objects.get(username = request.user)
    
    if zalogowany.groups.filter(name='klienci'):
        return redirect('profil_klienta')

    aktualny = datetime.date.today()
    miesiace = {1:"STY", 2:"LUT", 3:"MAR", 4:"KWI", 5:"MAJ", 6:"CZE",7:"LIP", 8:"SIE", 9:"WRZ", 10:"PAZ", 11:"LIS", 12:"GRU"}
    
    statystyki = dict()

    statystyki.update({'dzis': datetime.date.today()})
    statystyki.update({'liczbaKlientow' : Klient.objects.all().count()})
    statystyki.update({'liczbaAktywnych' : Klient.objects.filter(aktywny = True).count()})
    statystyki.update({'liczbaNieaktywnych' : statystyki['liczbaKlientow'] - statystyki['liczbaAktywnych']})
    statystyki.update({'ostatnich5' : Klient.objects.all().order_by('-id')[:5]})





    
    statystyki.update({'procentAktywnych' : round((statystyki['liczbaAktywnych'] / statystyki['liczbaKlientow']) * 100, 2)})
    
    statystyki.update({'liczbaMontazy' : Montaz.objects.all().count() })
    statystyki.update({'liczbaAktywnychMontazy' : Montaz.objects.filter(status = True).count() })
    statystyki.update({'liczbaZakonczonychMontazy' : Montaz.objects.filter(status = False).count() })
    statystyki.update({'procentAktywnychMontazy' : round((statystyki['liczbaAktywnychMontazy'] / statystyki['liczbaMontazy']) * 100, 2)})
    statystyki.update({'ostatnich5Montazy' : Montaz.objects.all().order_by('-id')[:5]})
    
    statystyki.update({'fakturyDzisiaj': Faktura.objects.filter(typ = 'faktura').filter(dataWystawienia = aktualny).count()})
    statystyki.update({'fakturyTenMiesiac': Faktura.objects.filter(typ = 'faktura').filter(nazwa__icontains = f'{miesiace[aktualny.month]}/{aktualny.year}/F').count()})
    statystyki.update({'fakturyPoprzedniMiesiac': Faktura.objects.filter(nazwa__icontains = f'{miesiace[aktualny.month - 1]}/{aktualny.year}/F').count()})

    liczbaWplatDzisiaj = Faktura.objects.filter(typ = 'płatność').filter(dataWystawienia = aktualny)
    liczbaWplatAktualnyMiesiac = Faktura.objects.filter(typ = 'płatność').filter(nazwa__icontains = f'{miesiace[aktualny.month]}/{aktualny.year}/P')
    liczbaWplatPoprzedniMiesiac = Faktura.objects.filter(typ = 'płatność').filter(nazwa__icontains = f'{miesiace[aktualny.month - 1]}/{aktualny.year}/P')
    
    sumaWplatDzisiaj = 0
    sumaWplatAktualnyMiesiac = 0
    sumaWplatPoprzedniMiesiac = 0

    for wplata in liczbaWplatDzisiaj:
        sumaWplatDzisiaj+= wplata.koszt
    
    for wplataAM in liczbaWplatAktualnyMiesiac:
        sumaWplatAktualnyMiesiac += wplataAM.koszt

    for wplataPM in liczbaWplatPoprzedniMiesiac:
        sumaWplatPoprzedniMiesiac += wplataPM.koszt

    statystyki.update({'sumaWplatDzisiaj': sumaWplatDzisiaj})    
    statystyki.update({'sumaWplatAktualnyMiesiac': sumaWplatAktualnyMiesiac})
    statystyki.update({'sumaWplatPoprzedniMiesiac': sumaWplatPoprzedniMiesiac})

    statystyki.update({'liczbaOtwartychZgloszen' : Zgloszenie.objects.filter(statusRozwiazany = False).count()})
    statystyki.update({'liczbaZamknietychZgloszen' : Zgloszenie.objects.filter(statusRozwiazany = True).count()})
    statystyki.update({'ostatnieZgloszenie' : Zgloszenie.objects.last()})
    

    return render(request, 'glowna/glowna.html', statystyki)


def logowanie(request):
    
    if request.user.is_authenticated:
        return redirect("glowna")
    
    

    
    
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['haslo']

        
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'Nie ma takiego użytkownika')
        
        
        user = authenticate(request, username = username, password = password)
        

        if user is not None:
            login(request, user)
            zalogowany = User.objects.get(username = request.user)
    
            if zalogowany.groups.filter(name='klienci'):
                return redirect('profil_klienta')
            else:
                return redirect('glowna')
        else:
            messages.error(request, 'Login lub hasło jest niepoprawne')

    return render(request, 'glowna/logowanie.html')

@login_required(login_url="logowanie")
def wylogowanie(request):
    logout(request)
    messages.error(request, 'Pomyślnie wylogowano')
    return redirect('logowanie')