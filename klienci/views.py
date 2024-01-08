from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Klient, KlientHistoria, Skan, Faktura, KontoBankowe, Umowa
from helpdesk.models import Zgloszenie, ZgloszenieOdpowiedzi
from zarzadzanie.models import Taryfa
from .forms import DodawanieNowegoKlienta
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.models import Group
from twilio.rest import Client # type: ignore
import datetime
from itertools import chain, count

#pdf
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.lib.styles import ParagraphStyle
#pdf


#csv
import csv

#csv

import os

from django.core.mail import send_mail, EmailMessage
from django.conf import settings

@login_required(login_url="logowanie")
def klienci(request):
    zalogowany = User.objects.get(username = request.user)
    
    if zalogowany.groups.filter(name='klienci'):
        return redirect('profil_klienta')
    
    ostatni = Klient.objects.order_by('id').last()
    paginacja = Paginator(Klient.objects.all(),3)
    strona = request.GET.get('strona')
    klienci = paginacja.get_page(strona)
    numeracja = "i" * klienci.paginator.num_pages

    x = Klient.objects.all()

    
    submitted = False
    if 'dodaj' in request.POST:
       
       
        form = DodawanieNowegoKlienta(request.POST)
        
        
        if form.is_valid():
        
            form.save()
            
            klient = Klient.objects.get(pesel = request.POST["pesel"])
            KlientHistoria.objects.create(uzytkownik=request.user, zmieniono="Utworzono konto użytkownika", klient = klient)
            
            login = request.POST['imie'] + request.POST['nazwisko'] + str(klient.id)
            haslo = request.POST["pesel"]
            
            grupa = Group.objects.get(name='klienci') 
            UserModel = get_user_model()
            user = UserModel.objects.create(username=login)
            user.set_password(haslo)
            user.groups.add(grupa)
            user.save()
            
            
            klient.uzytkownik = user
            klient.save()
            
            numerKonta = KontoBankowe.objects.filter(klient_id = None).order_by('?')[0]
    
            numerKonta.klient_id = klient
            numerKonta.save()
            
           

            
            if request.POST['email']:

                tresc = f'Dzień dobry, {klient.imie} {klient.nazwisko}, cieszymy się, że do nas dołączyłeś! Informujemy, że od dnia instalacji jest czas do 14 dni na podpisanie umowy lub odstąpenie. W razie pytań zapraszamy do kontaktu!'
                
                send_mail("Witamy w sieci", tresc, settings.EMAIL_HOST_USER, [request.POST['email']], fail_silently=False)
                KlientHistoria.objects.create(uzytkownik=request.user, zmieniono=f'Mail powitalny został wysłany na adres {request.POST["email"]}', klient = klient)
                return HttpResponseRedirect('/klienci?submitted=True')
            

            else:
                return HttpResponseRedirect('/klienci?submitted=True')

    else: 
        form = DodawanieNowegoKlienta
        if 'submitted' in request.GET:
            submitted = True
            

    if 'pokaz' in request.POST:
        
        paginacja = Paginator(Klient.objects.all(),1000)
        strona = request.GET.get('strona')
        klienci = paginacja.get_page(strona)
        numeracja = "i" * klienci.paginator.num_pages



    return render(request, "klienci/lista_klientow.html", {'klienci':klienci, 'form':form, 'submitted':submitted, 'ostatni': ostatni, 'numeracja':numeracja})

@login_required(login_url="logowanie")
def klient(request, id):
    zalogowany = User.objects.get(username = request.user)
    
    if zalogowany.groups.filter(name='klienci'):
        return redirect('profil_klienta')

    

    klient = Klient.objects.get(pk = id)
    form = DodawanieNowegoKlienta(request.POST or None, instance = klient)
    kontoBankowe = KontoBankowe.objects.get(klient_id = id)
    
    taryfaKlienta = klient.taryfa
    pakiety = klient.pakiety.all()
    idUzytkownika = klient.uzytkownik.id
    uzytkownik = klient.uzytkownik

    form2 = SetPasswordForm(uzytkownik, request.POST or None)

    if taryfaKlienta:

        lacznyAbonament = 0
        lacznyAbonament += taryfaKlienta.cena

        for pakiet in pakiety:
            lacznyAbonament += pakiet.cena
    
    else: lacznyAbonament = None
    
    
    skany = Skan.objects.all()
    faktury = Faktura.objects.filter(uzytkownik_id = id).order_by("-id")
    historia = KlientHistoria.objects.all().order_by('-data')
    umowy = Umowa.objects.filter(uzytkownik_id = id).order_by('-dataDodania')


    if 'przyciskEdytuj' in request.POST: 
        

        if request.POST['imie'] != klient.imie:
            KlientHistoria.objects.create(uzytkownik=request.user, zmieniono=f'Zmiania wartości "imię" z {klient.imie} na {request.POST["imie"]}', klient = klient)


        if form.is_valid():

            form.save()
            
        
            return HttpResponseRedirect(request.path_info)
        
    
    if 'przyciskHaslo' in request.POST: 
        
        if form.is_valid():
            form.save()
            
            
            KlientHistoria.objects.create(uzytkownik=request.user, zmieniono="Zmieniono hasło użytkownika", klient = klient)
            return HttpResponseRedirect(request.path_info)
        

    return render(request, "klienci/klient.html", {'form2': form2, 'klient': klient, "idUzytkownika": idUzytkownika, "lacznyAbonament":lacznyAbonament, 'form': form, 'skany':skany, 'historia':historia, 'faktury':faktury, "kontoBankowe":kontoBankowe, "taryfaKlienta":taryfaKlienta, 'pakiety':pakiety, 'umowy':umowy})

@login_required(login_url="logowanie")
def wyslij_mail(request):

    
    if request.method == 'POST':
       
        mail = request.POST['mail']
        tytul = request.POST['tytul']
        tresc = request.POST['tresc']
        
        
        wiadomosc = EmailMessage(tytul, tresc, settings.EMAIL_HOST_USER, [mail])
        
    
        if 'zalacznik' in request.FILES:
            zalaczniki = request.FILES.getlist('zalacznik')
            
            for zalacznik in zalaczniki:
                wiadomosc.attach(zalacznik.name, zalacznik.read(), zalacznik.content_type)
        
        
        
        try: 
             wiadomosc.send()

        except:
            mailStatus = False
            return render(request, "klienci/mail.html", {"mailStatus":mailStatus,  'id': request.POST['id']})
            
        mailStatus = True
        
                    
        klient = Klient.objects.get(id = request.POST['id'])
        KlientHistoria.objects.create(uzytkownik=request.user, zmieniono=f'Wiadomość została wysłana na maila {mail}', klient = klient)

        return render(request, "klienci/mail.html", {"mailStatus":mailStatus, 'id': request.POST['id'] })
    
    return render(request, "klienci/mail.html")


@login_required(login_url="logowanie")
def wyslij_sms(request):   
    zalogowany = User.objects.get(username = request.user)
    
    if zalogowany.groups.filter(name='klienci'):
        return redirect('profil_klienta')
    
    
    blad = 1
    if request.method == 'POST':
        
        try:
            
            sms = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
            numer = request.POST['numer']
            tresc = request.POST['tresc']
            message = sms.messages.create(
                
                to=numer, 
                from_= settings.TWILIO_NUMBER,
                body=tresc)

        
             
            klient = Klient.objects.get(id = request.POST['id'])
            KlientHistoria.objects.create(uzytkownik=request.user, zmieniono=f'SMS na numer {numer} został wysłany', klient = klient)
        
        except:
            return render(request, "klienci/sms.html", {"blad":blad})
            
    
    
        
    blad -= 1
    return render(request, "klienci/sms.html", {"blad":blad})

@login_required(login_url="logowanie")
def dodaj_skan(request):   
    zalogowany = User.objects.get(username = request.user)

    if zalogowany.groups.filter(name='klienci'):
        return redirect('profil_klienta')
    
    
    blad = 1

    
    if 'skasujSkan' in request.POST:
        print(request)

    
    if request.method == 'POST':
        
        try:
            nazwaSkanu = request.POST['nazwaSkanu']
            skan = request.FILES['skan']
            idKlienta = request.POST['id']
            klient = Klient.objects.get(id = request.POST['id'])
    
            Skan.objects.create(nazwaSkanu=nazwaSkanu, skan=skan, klient_id = idKlienta)
            KlientHistoria.objects.create(uzytkownik=request.user, zmieniono=f'Skan "{nazwaSkanu}" został dodany', klient = klient)
        except:
            return render(request, "klienci/skan.html", {"blad":blad, "idKlienta":request.POST['id']})
            
        
        
    blad -= 1
    return render(request, "klienci/skan.html", {"blad":blad, "idKlienta":request.POST['id']})

@login_required(login_url="logowanie")
def wystaw_fakture(request):   
    zalogowany = User.objects.get(username = request.user)
    
    if zalogowany.groups.filter(name='klienci'):
        return redirect('profil_klienta')


    if request.method == 'POST':

        pozycje = request.POST.getlist('pole')
        ceny = request.POST.getlist('cena')
        podatek = request.POST.getlist('podatek')
        sztuk = request.POST.getlist('ilosc')
        sposobPlatnosci = request.POST['rodzajPlatnosci']
        aktualny = datetime.date.today()
        iloscDni = request.POST['terminPlatnosciDni']
        terminPlatnosciDni = datetime.timedelta(int(iloscDni))
        terminPlatnosciData = terminPlatnosciDni + aktualny
        
        

        ostatni = Faktura.objects.last()
        pole = Faktura._meta.get_field("id")
        


        try:
            ostatni = Faktura.objects.last()
            pole = Faktura._meta.get_field("id")
            idOstatniego = getattr(ostatni, pole.attname)  # type: ignore
            
            idOstatniego += 1
            
            nazwaPliku = "plik" + str(idOstatniego)
        
        except:
            idOstatniego = 1
            nazwaPliku = "plik1"
        
        finally:
        
            miesiace = {1:"STY", 2:"LUT", 3:"MAR", 4:"KWI", 5:"MAJ", 
            6:"CZE",7:"LIP", 8:"SIE", 9:"WRZ", 10:"PAZ", 11:"LIS", 12:"GRU"
            }

            wynik = Faktura.objects.filter(nazwa__icontains = f'{miesiace[aktualny.month]}/{aktualny.year}/F')
            ilosc = wynik.count()

            if ilosc == 0:
                numerFaktury = 1
                
            else:
                numerFaktury = ilosc + 1

            
            nazwa = f'{numerFaktury}/{miesiace[aktualny.month]}/{aktualny.year}/F'
            

            klient = Klient.objects.get(id = request.POST['id'])
            numerKonta = KontoBankowe.objects.get(klient_id = klient)
 
            #Wyglad faktury
            faktura = canvas.Canvas(settings.MEDIA_ROOT + f'/faktury/{nazwaPliku}.pdf')
            pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
            faktura.setFont("Verdana", 17)
            faktura.setTitle(nazwa)
            faktura.drawString(30,790,f'Faktura VAT nr: {nazwa}')
            faktura.setFont("Verdana",10)
            faktura.drawString(400,790,f'Data wystawienia: {aktualny}')
            faktura.drawString(400,780,f'Termin płatności: {terminPlatnosciData}')
            faktura.setFont("Verdana", 15)
            faktura.drawString(80, 730, "Operator: ")
            faktura.drawString(380, 730, "Nabywca/odbiorca: ")
            faktura.setFont("Verdana", 12)
            faktura.drawString(80, 700, "Django Python Sp. z.o.o.")
            faktura.drawString(80, 685, "ul. Warszawska 290")
            faktura.drawString(80, 670, "34-120 Inwałd")
            faktura.drawString(80, 655, "NIP: 111-222-33-44")
            faktura.drawString(80, 620, f'Numer konta: {numerKonta.numerKonta}')
            faktura.drawString(380, 700, f'{klient.imie} {klient.nazwisko}')
            faktura.drawString(380, 685, f'{klient.ulicaZamieszkania} {klient.numerZamieszkania}/{klient.numerMieszkaniaZamieszkania}')
            faktura.drawString(380, 670, f'{klient.kodPocztowyZamieszkania} {klient.miastoZamieszkania}')
            faktura.setFont("Verdana", 10)
            faktura.drawString(20, 565, "Lp.")
            faktura.drawString(50, 565, "Usługa")
            faktura.drawString(310, 565, "J.m.")
            faktura.drawString(340, 565, "Ilosc")
            faktura.drawString(370, 565, "VAT")
            faktura.drawString(400, 565, "Podatek")
            faktura.drawString(450, 565, "Netto")
            faktura.drawString(500, 565, "Brutto")
            faktura.drawString(540, 565, "Cena SZT")
            wysokosc = 560
            licznik = 1
            x = 50
            y = 550
            podatekSuma = 0
            nettoSuma = 0
            bruttoSuma = 0
            faktura.line(15, wysokosc, 590, wysokosc)
            faktura.setFont("Verdana", 7)

            
            


            
            for pozycja,kwota, vat, szt in zip(pozycje, ceny, podatek, sztuk):

                    cena = float(kwota)
                    podatekCena = float(vat)/100
                    podatek = (cena * podatekCena)/(1 + podatekCena)
                    cenaNetto = cena - podatek
                    faktura.drawString(x-30,y,f'{licznik}')
                    faktura.drawString(x,y,f'{pozycja}')
                    faktura.drawString(x+260,y,'SZT')
                    faktura.drawString(x+290,y,f'{szt}')
                    faktura.drawString(x+320,y,f'{vat}%')
                    faktura.drawString(x+350,y,f'{round((podatek*int(szt)),2)}')
                    faktura.drawString(x+400,y,f'{round((cenaNetto*int(szt)),2)}')
                    faktura.drawString(x+450,y,f'{round((cena*int(szt)),2)}')
                    faktura.drawString(x+490,y,f'{kwota} PLN')
                    licznik += 1
                    y -= 15
                    wysokosc -= 15
                    podatekSuma += podatek*int(szt)
                    nettoSuma += cenaNetto*int(szt)
                    bruttoSuma += cena*int(szt)
                    faktura.line(15, wysokosc, 590, wysokosc)

            faktura.setFont("Verdana", 18)
            faktura.drawString(400, 320, "Podsumowanie")
            faktura.setFont("Verdana", 10)
            faktura.drawString(400, 300, f'Podatek: {round(podatekSuma,2)} PLN')
            faktura.drawString(400, 290, f'Netto: {round(nettoSuma,2)} PLN')
            faktura.drawString(400, 280, f'Brutto: {round(bruttoSuma, 2)} PLN')
            faktura.drawString(400, 270, f'Sposób płatności: {sposobPlatnosci}')
            faktura.drawString(400, 260, f'Saldo przed: {klient.stanKonta}')
            faktura.setFont("Verdana", 18)
            faktura.drawString(200, 200, f'Łączna kwota do zapłaty: {round(bruttoSuma, 2)} PLN')
            
            
            
            faktura.showPage()
            faktura.save()
            
            klient.stanKonta -= round(bruttoSuma, 2)
            klient.save()

            
        Faktura.objects.create(typ = "faktura", uzytkownik = klient, nazwa=nazwa, koszt=round(bruttoSuma,2), saldoPo=klient.stanKonta,  faktura=f'/faktury/{nazwaPliku}.pdf', dataWystawienia=aktualny, terminPlatnosci = terminPlatnosciData, sposobPlatnosci = sposobPlatnosci)
        

    return render(request, "klienci/lista_klientow.html", {})








@login_required(login_url="logowanie")
def dodaj_wplate(request):   
    zalogowany = User.objects.get(username = request.user)
    
    if zalogowany.groups.filter(name='klienci'):
        return redirect('profil_klienta')



    if request.method == 'POST':
        aktualny = datetime.date.today()
        klient = Klient.objects.get(id = request.POST['id'])
        kwota = request.POST['kwota']
        notatka = request.POST['notatka']

        miesiace = {1:"STY", 2:"LUT", 3:"MAR", 4:"KWI", 5:"MAJ", 6:"CZE",7:"LIP", 8:"SIE", 9:"WRZ", 10:"PAZ", 11:"LIS", 12:"GRU"}

        wynik = Faktura.objects.filter(nazwa__icontains = f'{miesiace[aktualny.month]}/{aktualny.year}/P')
        ilosc = wynik.count()

        if ilosc == 0:
            numerPlatnosci = 1
                
        else:
            numerPlatnosci = ilosc + 1

            
        klient.stanKonta += float(kwota)
        klient.save()

        nazwa = f'{numerPlatnosci}/{miesiace[aktualny.month]}/{aktualny.year}/P'
        Faktura.objects.create(typ = "płatność", uzytkownik = klient, nazwa=nazwa, koszt=round(float(kwota),2), saldoPo=klient.stanKonta , dataWystawienia=aktualny, notatka = notatka)


    return render(request, "klienci/lista_klientow.html", {})

@login_required(login_url="logowanie")
def generuj_raportCSV(request):   
    zalogowany = User.objects.get(username = request.user)
    
    if zalogowany.groups.filter(name='klienci'):
        return redirect('profil_klienta')



    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=raport.csv'
    raport = csv.writer(response)
    klient = Klient.objects.get(id = request.POST['id'])
    
    if '"dataStartowa"' and "dataKoncowa" in request.POST:
        

        platnosci = Faktura.objects.filter(uzytkownik = klient).filter(dataWystawienia__range=(request.POST['dataStartowa'], request.POST['dataKoncowa'])).order_by('-dataDodania')
        
        raport.writerow(['typ', 'nazwa', 'kwota', 'saldo po', 'data wystawienia', 'termin płatności'])

        for platnosc in platnosci:
            raport.writerow([platnosc.typ, platnosc.nazwa, platnosc.koszt, platnosc.saldoPo, platnosc.dataWystawienia, platnosc.terminPlatnosci])
    
    else:
        platnosci = Faktura.objects.filter(uzytkownik = klient).order_by('-dataDodania')

        raport.writerow(['typ', 'nazwa', 'kwota', 'saldo po', 'data wystawienia', 'termin płatności'])

        for platnosc in platnosci:
            raport.writerow([platnosc.typ, platnosc.nazwa, platnosc.koszt, platnosc.saldoPo, platnosc.dataWystawienia, platnosc.terminPlatnosci])
    
    
    return response 

@login_required(login_url="logowanie")
def generuj_umowe(request):
    
    zalogowany = User.objects.get(username = request.user)
    
    if zalogowany.groups.filter(name='klienci'):
        return redirect('profil_klienta')



    if request.method == 'POST':


        aktualny = datetime.date.today()
        dataOd = request.POST['dataOd']
        dataDo = request.POST['dataDo']
        taryfa = request.POST['taryfa']
        klient = Klient.objects.get(id = request.POST['id'])
        numerKonta = KontoBankowe.objects.get(klient_id = klient)
        taryfaKlienta = klient.taryfa
        ostatni = Umowa.objects.last()
        
        pole = Faktura._meta.get_field("id")
        
        try:
            idOstatniego = getattr(ostatni, pole.attname) # type: ignore
            idOstatniego += 1
            nazwaPliku = "umowa" + str(idOstatniego)
        
        except:
            idOstatniego = 1
            nazwaPliku = "umowa1"
        
        finally:
        
            miesiace = {1:"STY", 2:"LUT", 3:"MAR", 4:"KWI", 5:"MAJ", 6:"CZE",7:"LIP", 8:"SIE", 9:"WRZ", 10:"PAZ", 11:"LIS", 12:"GRU"}

            wynik = Umowa.objects.filter(nazwa__icontains = f'{miesiace[aktualny.month]}/{aktualny.year}/U')
            ilosc = wynik.count()

            if ilosc == 0:
                numerUmowy = 1
                
            else:
                numerUmowy = ilosc + 1

            nazwa = f'{numerUmowy}/{miesiace[aktualny.month]}/{aktualny.year}/U'
            
        #Wyglad faktury
        umowa = canvas.Canvas(settings.MEDIA_ROOT + f'/umowy/{nazwaPliku}.pdf')
        pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
        umowa.setFont("Verdana", 17)
        umowa.setTitle(nazwa)
        umowa.drawString(30,790,f'Umowa nr: {nazwa}')
        umowa.setFont("Verdana", 15)
        umowa.drawString(80, 730, "Operator: ")
        umowa.drawString(380, 730, "Nabywca/odbiorca: ")
        umowa.setFont("Verdana", 12)
        umowa.drawString(30,750,f'Umowa zawarta dnia {aktualny} pomiędzy:')

        umowa.drawString(80, 700, "Django Python Sp. z.o.o.")
        umowa.drawString(80, 685, "ul. Warszawska 290")
        umowa.drawString(80, 670, "34-120 Inwałd")
        umowa.drawString(80, 655, "NIP: 111-222-33-44")
        

        umowa.drawString(380, 700, f'{klient.imie} {klient.nazwisko}')
        umowa.drawString(380, 685, f'{klient.ulicaZamieszkania} {klient.numerZamieszkania}/{klient.numerMieszkaniaZamieszkania}')
        umowa.drawString(380, 670, f'{klient.kodPocztowyZamieszkania} {klient.miastoZamieszkania}')
        umowa.setFont("Verdana", 15)
        umowa.drawString(10, 620, '§1 Warunki umowy')
        
        umowa.setFont("Verdana", 11)

        umowa.drawString(15, 600, f'Klientowi został przyznany indywidualny numer konta do płacenia: {numerKonta.numerKonta}')
        umowa.drawString(15, 585, f'Taryfa wybrana przez klienta: {taryfa} o następujących parametrach: ')
        umowa.drawString(15, 570, f'Download: {taryfaKlienta.pobieranie} mb/s')
        umowa.drawString(15, 555, f'Upload: {taryfaKlienta.wysylanie} mb/s')
        umowa.drawString(15, 540, f'Umowa obowiązuje od {dataOd} do {dataDo}')
        umowa.drawString(15, 525, f'Miesięczny abonament wynosi {taryfaKlienta.cena} PLN (W tym VAT {taryfaKlienta.podatek}%)')
        umowa.drawString(15, 510, f'Faktury za usługi będą wystawiane co miesiąc na początku danego miesiąca. Termin płatnosci każdej')
        umowa.drawString(15, 495, f'faktury wynosi 14 dni od daty jej wystawienia. Wszystkie faktury będą dostępnego w panelu klienta')
        umowa.drawString(15, 480, f'lub w przypadku wyrażenia zgody wysyłane drogą elektroniczną')
        umowa.drawString(15, 465, f'Dostęp do panelu klienta zostaje nadany w dniu wygenerowania konta, dane do logowania znajdują ')
        umowa.drawString(15, 450, f'się w biurze obługi klienta. ')
        

        umowa.setFont("Verdana", 15)
        umowa.drawString(10, 415, '§2 Regulamin')
        
        umowa.setFont("Verdana", 11)
        umowa.drawString(15, 395, f'1) Przepustowosć łącza jest gwarantowana za pomocą połączania erhernet, operator nie gwarantuje')
        umowa.drawString(15, 380, f'prędkości deklarowanej w umowie w sieci bezprzewodowej ani nie gwarantuje zasięgu w całym domu. ')
        umowa.drawString(15, 365, f'2) W przypadku braku terminowych wpłat za abonament operator ma prawo w trybie tatychmiastowym')
        umowa.drawString(15, 350, f'wyłączyć swoje usługi')
        umowa.drawString(15, 335, f'3) W przypadku wcześniejszego zerwania umowy operator ma prawo nałożyć karę za zerwanie umowy.')
        umowa.drawString(15, 320, f'Wzór na wysokość kary jest następujący: ')
        umowa.drawString(15, 305, f'30 PLN brutto za każdy pozostały miesiąc umowy + zwrot kosztów instalacji')
        umowa.drawString(15, 290, f'4) W przypadku awarii operator deklaruje usunięcie usterki do 48h od chwili zgłoszenia. W przypadku')
        umowa.drawString(15, 275, f'gdy usterka nie zostanie naprawiona do 48h od chwili zgłoszenia, klient ma prawo złożyć reklamację')
        umowa.drawString(15, 260, f'w formie pisemnej.')
        umowa.drawString(15, 245, f'5) W przypadku serwisu, który wyniknął z winy klienta, operator ma prawo wystawić fakturę za serwis.')
        umowa.drawString(15, 230, f'Kwota zależy od ilości czasu pracy serwisantów oraz ilości zużytych materiałów')
        umowa.drawString(15, 215, f'6) Operator deklaruje dostępność usługi na poziomie 99% w skali roku, zastrzegając sobie prawo do')
        umowa.drawString(15, 200, f'nieprzewidzianych awarii lub modernizacji sieci')
        umowa.drawString(15, 185, f'7) Dostawca internetu nie bierze odpowiedzialności za działanie klientów w sieci.')
        umowa.drawString(15, 170, f'8) Udostępnianie internetu poza lokal bez wiedzy operatora jest zabronione')
        umowa.drawString(15, 155, f'9) W przypadku nieprzestrzegania regulaminu lub łamania prawa podczas korzystania z usług, operator')
        umowa.drawString(15, 140, f'zastrzega sobie prawo do zerwania umowy z zachowaniem okresu wypowiedzenia')
        umowa.drawString(15, 125, f'10) Klient ma prawo wglądu do danych, które operator wykorzystuje')
        umowa.drawString(15, 110, f'11) Abonent ma prawo wciągu jednego roku kalendarzowego zawiesić usługi na okres dwóch miesięcy.')
        umowa.drawString(15, 95,  f'Za ten okres faktury niebędą wystawianie')
        umowa.drawString(15, 80,  f'12) Wydany sprzęt przez operatora jest powierzony klientowi na zasadzie dzierżawy i po zakończeniu')
        umowa.drawString(15, 65,  f'umowy sprzęt powinien zostać zwrócony w stanie sprawnym. W przypadku braku zwrotu lub zniszczeniu ')
        umowa.drawString(15, 50,  f'urządzenia, operator ma prawo naliczyc fakturę za sprzęt.')
        umowa.drawString(15, 35,  f'13)Po zakończeniu taryfy, umowa staje się bezterminowa i obowiązuje miesięczny okres wypowiedzenia')

        umowa.showPage()
        umowa.setFont("Verdana", 15)

        umowa.drawString(10, 800, '§3 Zgody')
        umowa.setFont("Verdana", 11)
        umowa.drawString(15, 780, f'Skreślić niepotrzebne')
        umowa.drawString(15, 750, f'Wyrażam / Nie wyrażam zgodę na otrzymywanie faktur w postaci elektronicznej na adres mailowy.')
        umowa.drawString(15, 720, f'Wyrażam / Nie wyrażam zgodę na przetwaranie danych osobywch w celach marketingowych.')
        umowa.drawString(15, 690, f'Wyrażam / Nie wyrażam zgodę na informowanie mnie o awariach lub przerwach technicznych drogą')
        umowa.drawString(15, 675, f'mailową lub telefoniczną.')

        
        umowa.drawString(15, 600, f'Informujemy, że administratorem Pani/Pana danych osobowych jest Django Python Sp. z.o.o. z siedzibą ')
        umowa.drawString(15, 585, f'w Inwałd przy ul. Warszawska 290.')

        umowa.drawString(80, 500, f'...............................')
        umowa.drawString(80, 485, f'Podpis uprawionego pracownika')

        umowa.drawString(380, 500, f'..............................')
        umowa.drawString(380, 485, f'Podpis klienta')

        umowa.save()   

            
        Umowa.objects.create(uzytkownik = klient, nazwa=nazwa, umowa=f'/umowy/{nazwaPliku}.pdf', dataDo = dataDo, dataOd = dataOd)

    return render(request, "klienci/lista_klientow.html", {})



@login_required(login_url="logowanie")
def profil_klienta(request):

    zalogowany = User.objects.get(username = request.user)
    klient = Klient.objects.get(uzytkownik = zalogowany)

    form = PasswordChangeForm(request.user, request.POST)
    
    if 'przyciskHaslo' in request.POST: 
        
        if form.is_valid():
            form.save()
            
        return HttpResponseRedirect(request.path_info)


    if 'dodajZgloszenie' in request.POST:
        klient = Klient.objects.get(id = request.POST['id'])
        
        
        if 'zalacznik' in request.FILES:
            Zgloszenie.objects.create(temat = request.POST['temat'], tresc = request.POST['tresc'], klient = klient, zalacznik = request.FILES['zalacznik'])
        
        else:
            Zgloszenie.objects.create(temat = request.POST['temat'], tresc = request.POST['tresc'], klient = klient)

        
        return HttpResponseRedirect(request.path_info)
        
        
    if zalogowany.groups.filter(name='klienci'):
        odmowa = False

        kontoBankowe = KontoBankowe.objects.get(klient_id = klient.id)
        zgloszenia = Zgloszenie.objects.filter(klient = klient)
        taryfaKlienta = klient.taryfa
        pakiety = klient.pakiety.all()
        faktury = Faktura.objects.filter(uzytkownik = klient).order_by("-id")
        lacznyAbonament = 0
        lacznyAbonament += taryfaKlienta.cena

        for pakiet in pakiety:
            lacznyAbonament += pakiet.cena

        return render(request, "klienci/profil_klienta.html", {'faktury':faktury, "zgloszenia": zgloszenia, "lacznyAbonament": lacznyAbonament, "odmowa":odmowa, 'form': form, 'klient':klient, 'kontoBankowe':kontoBankowe, 'taryfaKlienta':taryfaKlienta, 'pakiety':pakiety})
    
    else:
        odmowa = True
        return render(request, "klienci/profil_klienta.html", {"odmowa":odmowa})
    
   
@login_required(login_url="logowanie")
def wyslij_fakture(request, id):
    faktura = Faktura.objects.get(pk = id)
    
    klient = Klient.objects.get(id = faktura.uzytkownik_id)
    
    mail = klient.email
    tytul = "Faktura VAT"
    tresc = "W załączniku znajduje się faktura VAT"
    wiadomosc = EmailMessage(tytul, tresc, settings.EMAIL_HOST_USER, [mail])
    wiadomosc.attach_file(f'pliki/{faktura.faktura}')
    
    wiadomosc.send()
    
    


            
    
    


 
    return render(request, "klienci/klient.html", {})

@login_required(login_url="logowanie")
def umowa_podpisana(request, id):
    
    umowa = Umowa.objects.get(pk = id)
    klient = Klient.objects.get(pk = umowa.uzytkownik_id)
    

    umowa.czyPodpisana = True
    umowa.save()
            
    
    


 
    return redirect(f"/klienci/id/{klient.id}")

            
@login_required(login_url="logowanie")
def umowa_wyslij(request, id):
    umowa = Umowa.objects.get(pk = id)
    
    klient = Klient.objects.get(id = umowa.uzytkownik_id)
    

    mail = klient.email
    tytul = "Umowa"
    tresc = f"W załączniku znajduje się umowa nr {umowa.nazwa}. Prosimy o odesłanie podpisanej umowy w postaci skanu lub pocztą tradycyjną"
    wiadomosc = EmailMessage(tytul, tresc, settings.EMAIL_HOST_USER, [mail])
    wiadomosc.attach_file(f'pliki/{umowa.umowa}')
    
    try: 
        wiadomosc.send()

    except:
        mailStatus = False
        return render(request, "klienci/mail.html", {"mailStatus":mailStatus,  'id': klient.id})
            
    mailStatus = True
        
    KlientHistoria.objects.create(uzytkownik=request.user, zmieniono=f'Umowa {umowa.nazwa} została wysłana na maila {mail}', klient = klient)

    return render(request, "klienci/mail.html", {"mailStatus":mailStatus, 'id': klient.id})
        