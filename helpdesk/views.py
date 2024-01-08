from itertools import count
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Zgloszenie, ZgloszenieOdpowiedzi
from django.contrib.auth.models import Group, Permission
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from klienci.models import Klient
from django.conf import settings
from twilio.rest import Client

@login_required(login_url="logowanie")
def zgloszenia(request):
    
    zalogowany = User.objects.get(username = request.user)
    
    if zalogowany.groups.filter(name='klienci'):
        return redirect('profil_klienta')
    

    zgloszenia = Zgloszenie.objects.all()
    
    if 'archiwum' in request.POST:
        zgloszenie = Zgloszenie.objects.get(id = request.POST['id'])

        zgloszenie.statusRozwiazany = True
        zgloszenie.save()
        

    return render(request, 'helpdesk/zgloszenia.html', {'zgloszenia':zgloszenia})   

@login_required(login_url="logowanie")
def zgloszenie(request, id):

    
    
    zalogowany = User.objects.get(username = request.user)
    zgloszenie = Zgloszenie.objects.get(pk = id)
    zgloszenieOdpowiedzi = ZgloszenieOdpowiedzi.objects.filter(zgloszenie_id = id)
    
    

    klient =zgloszenie.klient
    print(klient.email)
    
    idKlienta = klient.id



    if zalogowany.groups.filter(name='klienci'):
        klientZalogowany = Klient.objects.get(uzytkownik = zalogowany)
        if klientZalogowany != klient:
            return redirect('profil_klienta')
        
        
        dostep = False
        
    else:
        
        dostep = True



    
    
    
    if 'odpowiedz' in request.POST:

        
        
        if 'zalacznik' in request.FILES:
            
            if dostep == False:

                klient = Klient.objects.get(uzytkownik = zalogowany)
                ZgloszenieOdpowiedzi.objects.create(klient = klient, tresc=request.POST['tresc'] ,zgloszenie=zgloszenie, zalacznik = request.FILES['zalacznik'])

            else:
                ZgloszenieOdpowiedzi.objects.create(uzytkownik = request.user, tresc=request.POST['tresc'] ,zgloszenie=zgloszenie, zalacznik = request.FILES['zalacznik'])
        
            
        
        else:
            

            if dostep == False:

                klient = Klient.objects.get(uzytkownik = zalogowany)
                ZgloszenieOdpowiedzi.objects.create(klient = klient, tresc=request.POST['tresc'] ,zgloszenie=zgloszenie)

            else:
                ZgloszenieOdpowiedzi.objects.create(uzytkownik = request.user, tresc=request.POST['tresc'] ,zgloszenie=zgloszenie)

            

        if 'wyslijMail' in request.POST:
            mail = klient.email
            tytul = f"Odpowiedź na zgłoszenie nr: {zgloszenie.id}"
            tresc = "W twoim zgłoszeniu w Helpdesku znajduje się nowa odpowiedź od operatora."
            wiadomosc = EmailMessage(tytul, tresc, settings.EMAIL_HOST_USER, [mail])

            wiadomosc.send()

        if 'wyslijSMS' in request.POST:
            sms = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
            numer = f'+48{klient.numerGSM}'
            tresc = f'W twoim zgłoszeniu w Helpdesku o numerze {zgloszenie.id} znajduje się nowa odpowiedź od operatora'
            message = sms.messages.create(
                
                to=numer, 
                from_= settings.TWILIO_NUMBER,
                body=tresc)

        return HttpResponseRedirect(request.path_info)

    return render(request, "helpdesk/zgloszenie.html", {'dostep':dostep, 'zgloszenie': zgloszenie, 'odpowiedzi':zgloszenieOdpowiedzi, 'idKlienta':idKlienta, 'klient':klient})




    