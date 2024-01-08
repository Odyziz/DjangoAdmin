from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from klienci.models import *
from django.http import HttpResponseRedirect
import csv
import io
from .models import Taryfa, PakietDodatkowy
from klienci.models import Klient
from .forms import DodawanieNowejTaryfy
from django.contrib.auth.models import User, Group




@login_required(login_url="logowanie")
def spisAdresow(request):
    wojewodztwa = Wojewodztwo.objects.all()
    powiaty = Powiat.objects.all()
    gminy = Gmina.objects.all()
    miasta = Miasto.objects.all()
    ulice = Ulica.objects.all()

    return render(request, 'zarzadzanie/spisAdresow.html', {"wojewodztwa":wojewodztwa, 'powiaty':powiaty, 'gminy':gminy, 'miasta': miasta, 'ulice':ulice})

@login_required(login_url="logowanie")
def dodajAdres(request):


    return render(request, 'zarzadzanie/spisAdresow.html', {})



@login_required(login_url="logowanie")
def spisNumerow(request):
    
    kontaBankowe = KontoBankowe.objects.all()
    kontaBankoweKlient = KontoBankowe.objects.filter(klient_id = None)
    kontaBankoweIlosc = kontaBankowe.count()
    kontaBankoweKlientIlosc = kontaBankoweKlient.count()


    


    if 'przyciskNumery' in request.POST:

        

        if 'numerKonta' in request.POST:
            numery = request.POST.getlist('numerKonta')
            
            for numer in numery:
                
                if numer.isdigit():

                    try:
                        KontoBankowe.objects.get(numerKonta = numer)
                    except KontoBankowe.DoesNotExist:
                        KontoBankowe.objects.create(numerKonta = numer)
        
        if 'arkusz' in request.FILES:
            with io.TextIOWrapper(request.FILES["arkusz"], encoding="utf-8") as arkusz:
                numery = csv.DictReader(arkusz)

                
                
                for numer in numery:
                    if numer['Numer Konta'].isdigit():
                        try:
                            KontoBankowe.objects.get(numerKonta = numer['Numer Konta'])
                        except KontoBankowe.DoesNotExist:
                            KontoBankowe.objects.create(numerKonta = numer['Numer Konta'])
                

        return HttpResponseRedirect(request.path_info)



    return render(request, 'zarzadzanie/spisNumerow.html', {'kontaBankowe': kontaBankowe, 'kontaBankoweKlientIlosc': kontaBankoweKlientIlosc, 'kontaBankoweIlosc': kontaBankoweIlosc,})

@login_required(login_url="logowanie")
def spisTaryf(request):
    
    taryfy = Taryfa.objects.all()
    liczbaKlientow = list()
    form = DodawanieNowejTaryfy(request.POST or None)

    if 'dodaj' in request.POST:
        
        

        if form.is_valid():
            

            
            form.save()
            return HttpResponseRedirect(request.path_info)

        else: 
            form = DodawanieNowejTaryfy



    for taryfa in taryfy:
        klienci = Klient.objects.filter(taryfa = taryfa)
        liczbaKlientow.append(klienci.count())
        

    taryfaLiczba = zip(taryfy, liczbaKlientow)


    
        



    return render(request, 'zarzadzanie/spisTaryf.html', {'form': form, 'taryfaLiczba':taryfaLiczba})

@login_required(login_url="logowanie")
def taryfaSzczegoly(request, id):
    
    taryfa = Taryfa.objects.get(pk = id)
    klienci = Klient.objects.filter(taryfa_id = taryfa.id)
    
    



    return render(request, 'zarzadzanie/taryfa.html', {'taryfa':taryfa, 'klienci':klienci})



@login_required(login_url="logowanie")
def generuj_raport(request):
    
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')

    taryfy = Taryfa.objects.all()
    taryfyNazwy = list()
    liczbaKlientow = list()

    for taryfa in taryfy:
        klienci = Klient.objects.filter(taryfa = taryfa)
        liczbaKlientow.append(klienci.count())
        taryfyNazwy.append(f'{taryfa.nazwaTaryfy} suma: {klienci.count()}')


    response = HttpResponse(content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename=raport.png'
    

    pozycjeTaryf = np.arange(len(liczbaKlientow))
    x = plt.figure(figsize=(12,5))
    plt.bar(pozycjeTaryf, liczbaKlientow, color = '#2a2ac7')
    plt.xticks(pozycjeTaryf, taryfyNazwy) 
    plt.xlabel('Taryfa', fontsize=12, color='#323232')
    plt.ylabel('Liczba klientów', fontsize=12, color='#323232')
    plt.title('Statystyki taryf', fontsize=16, color='#323232')    
    plt.savefig(response)
    plt.switch_backend('Agg')
    plt.close(x)
    
    return response

    
@login_required(login_url="logowanie")
def spisPakietow(request):
    
    pakiety = PakietDodatkowy.objects.all()
    liczbaKlientow = list()

    for pakiet in pakiety:
        klienci = Klient.objects.filter(pakiety = pakiet)
        liczbaKlientow.append(klienci.count())


    pakietyLiczba = zip(pakiety, liczbaKlientow)


    return render(request, 'zarzadzanie/spisPakietow.html', {'pakietyLiczba':pakietyLiczba})

@login_required(login_url="logowanie")
def pakietSzczegoly(request, id):
    
    pakiet = PakietDodatkowy.objects.get(pk = id)
    
    
    klienci = Klient.objects.filter(pakiety = pakiet.id)



    return render(request, 'zarzadzanie/pakiet.html', {'pakiet':pakiet, 'klienci':klienci})

@login_required(login_url="logowanie")
def spisUzytkownikow(request):



    def liczba_uzytkownikow(grupa):
        return grupa.user_set.count()
    
    
    grupy = Group.objects.all()
    iloscUzytkownikow = list()
    
    for grupa in grupy:
        iloscUzytkownikow.append(liczba_uzytkownikow(Group.objects.get(id = grupa.id)))
    


    grupyLiczba = zip(grupy, iloscUzytkownikow)


    

    return render(request, 'zarzadzanie/spisUzytkownikow.html', {'grupyLiczba':grupyLiczba})

@login_required(login_url="logowanie")
def uzytkownicy(request, nazwa):
    grupa = Group.objects.get(name = nazwa)
    
    uzytkownicy = User.objects.filter(groups__name=nazwa)

    
    
    

    return render(request, 'zarzadzanie/uzytkownicy.html', {'grupa':grupa, 'uzytkownicy':uzytkownicy})



@login_required(login_url="logowanie")
def zarzadzanie(request):

    
    
    kontaBankoweIlosc = KontoBankowe.objects.all().count()
    kontaBankoweKlientIlosc = KontoBankowe.objects.filter(klient_id = None).count()
    taryfyIlosc = Taryfa.objects.all().count()
    pakietyDodatkoweIlosc = Taryfa.objects.all().count()
    uzytkownicy = User.objects.all().count()
    
    return render(request, 'zarzadzanie/zarzadzanie.html', {'uzytkownicy': uzytkownicy, 'pakietyDodatkoweIlosc': pakietyDodatkoweIlosc, 'taryfyIlosc':taryfyIlosc, 'kontaBankoweKlientIlosc': kontaBankoweKlientIlosc, 'kontaBankoweIlosc': kontaBankoweIlosc})

@login_required(login_url="logowanie")
def rejestracja(request):
    form = UserCreationForm()

    if request.method=="POST":
        form = UserCreationForm(request.POST)

        if form.is_valid:
            
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "Stworzono nowego użytkownika")

    return render(request, 'zarzadzanie/rejestracja.html',{"form": form})