import email
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont 
from django.contrib.auth.models import User
from requests import Request
from zarzadzanie.models import Taryfa
from klienci.models import Klient
from klienci.views import Klient, Faktura, KontoBankowe
from django.conf import settings
from django.core.mail import EmailMessage
import csv





@login_required(login_url="logowanie")
def finanse(request):

    miesiace = {1:"Styczeń", 2:"Luty", 3:"Marzecz", 4:"Kwiecień", 5:"Maj", 6:"Czerwiec",7:"Lipiec", 8:"Sierpień", 9:"Wrześień", 10:"Październik", 11:"Listopad", 12:"Grudzień"}

    aktualny = datetime.date.today()

    miesiac = miesiace[aktualny.month]
    rok = aktualny.year

    
    platnosci = Faktura.objects.filter(dataWystawienia = aktualny)
    klienci = Klient.objects.filter(email__isnull=False)
    



    return render(request, 'finanse/finanse.html', {'platnosci':platnosci, 'miesiac':miesiac, 'rok':rok, 'klienci':klienci})   

@login_required(login_url="logowanie")
def wyslij_maile(request):

    if 'wszyscyMaile' in request.POST:
        
        tytul = request.POST['tytul']
        tresc = request.POST['tresc']
        klienci = Klient.objects.filter(email__isnull=False)
        
        print(request.POST)


        
        klienci = Klient.objects.filter(email__isnull=False)
        for klient in klienci:
        
        
            wiadomosc = EmailMessage(tytul, tresc, settings.EMAIL_HOST_USER, [klient.email])
            
        
            if 'zalacznik' in request.FILES:
                zalaczniki = request.FILES.getlist('zalacznik')
                
                
                for zalacznik in zalaczniki:
                    wiadomosc.attach(zalacznik.name, zalacznik.read(), zalacznik.content_type)
            

            wiadomosc.send()
        

    if 'wybraniMaile' in request.POST:
        print(request.POST)


    return render(request, 'finanse/finanse.html', {})   


@login_required(login_url="logowanie")
def wystaw_faktury(request):
    
    
    if request.method == 'POST':

        
        klienci = Klient.objects.filter(aktywny=True).order_by('?')
        aktualny = datetime.date.today()
        
        


        for klient in klienci:
            ostatni = Faktura.objects.last()
            pole = Faktura._meta.get_field("id")
        
       

            try:
                idOstatniego = getattr(ostatni, pole.attname) # type: ignore
                idOstatniego += 1
                nazwaPliku = "plik" + str(idOstatniego)
        
            except:
                idOstatniego = 1
                nazwaPliku = "plik1"
        
            finally:
        
                miesiace = {1:"STY", 2:"LUT", 3:"MAR", 4:"KWI", 5:"MAJ", 6:"CZE",7:"LIP", 8:"SIE", 9:"WRZ", 10:"PAZ", 11:"LIS", 12:"GRU"}

                wynik = Faktura.objects.filter(nazwa__icontains = f'{miesiace[aktualny.month]}/{aktualny.year}/F')
                ilosc = wynik.count()

                if ilosc == 0:
                    numerFaktury = 1
                    
                else:
                    numerFaktury = ilosc + 1

            
            

                nazwa = f'{numerFaktury}/{miesiace[aktualny.month]}/{aktualny.year}/F'
                numerKonta = KontoBankowe.objects.get(klient_id = klient)
                taryfaKlienta = klient.taryfa
                
                miesiace2 = {
                    1:f"01.01 - 31.01.{aktualny.year}", 
                    2:f"01.02 - 28.02.{aktualny.year}", 
                    3:f"01.03 - 31.03.{aktualny.year}", 
                    4:f"01.04 - 30.04.{aktualny.year}", 
                    5:f"01.05 - 31.05.{aktualny.year}", 
                    6:f"01.06 - 30.06.{aktualny.year}",
                    7:f"01.07 - 31.07.{aktualny.year}", 
                    8:f"01.08 - 31.08.{aktualny.year}", 
                    9:f"01.09 - 30.09.{aktualny.year}",
                    10:f"01.10 - 31.10.{aktualny.year}", 
                    11:f"01.11 - 30.11.{aktualny.year}", 
                    12:f"01.12 - 31.12.{aktualny.year}"
                }

                 
                if aktualny.year % 4 == 0 and (aktualny.year % 400 == 0 or aktualny.year % 100 != 0):
                    miesiace2.update({2:f"01.02 - 29.02.{aktualny.year}"})
            
            
            
 



                #Wyglad faktury
                faktura = canvas.Canvas(settings.MEDIA_ROOT + f'/faktury/{nazwaPliku}.pdf')
                pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
                faktura.setFont("Verdana", 17)
                faktura.setTitle(nazwa)
                faktura.drawString(30,790,f'Faktura VAT nr: {nazwa}')
                
                faktura.setFont("Verdana",10)
                faktura.drawString(400,790,f'Data wystawienia: {aktualny}')
                faktura.drawString(400,780,f'Termin płatności: ')
                
        
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

                cena = float(taryfaKlienta.cena)
                podatekCena = float(taryfaKlienta.podatek)/100    
                podatek = (cena * podatekCena)/(1 + podatekCena)
                cenaNetto = cena - podatek

                
                faktura.drawString(x-30,y,f'{licznik}')
                faktura.drawString(x,y,f'{taryfaKlienta.nazwaTaryfy} za okres {miesiace2[aktualny.month]}')
                faktura.drawString(x+260,y,'SZT')
                faktura.drawString(x+290,y,f'1')
                faktura.drawString(x+320,y,f'{int(taryfaKlienta.podatek)}%')
                faktura.drawString(x+350,y,f'{round((podatek),2)}')
                faktura.drawString(x+400,y,f'{round((cenaNetto),2)}')
                faktura.drawString(x+450,y,f'{round((cena),2)}')
                faktura.drawString(x+490,y,f'{taryfaKlienta.cena} PLN')
                
                podatekSuma += podatek
                nettoSuma += cenaNetto
                bruttoSuma += cena
            
                faktura.line(15, wysokosc, 590, wysokosc)

                pakiety = klient.pakiety.all()
                for pakiet in pakiety:
                    y -= 15
                    wysokosc -= 15
                    licznik += 1
                    
                    cena = float(pakiet.cena)
                    podatekCena = float(pakiet.podatek)/100
                    
                    
                    podatek = (cena * podatekCena)/(1 + podatekCena)
                    cenaNetto = cena - podatek

                    
                    faktura.drawString(x-30,y,f'{licznik}')
                    faktura.drawString(x,y,f'{pakiet.nazwaPakietu} za okres {miesiace2[aktualny.month]}')
                    faktura.drawString(x+260,y,'SZT')
                    faktura.drawString(x+290,y,f'1')
                    faktura.drawString(x+320,y,f'{int(pakiet.podatek)}%')
                    faktura.drawString(x+350,y,f'{round((podatek),2)}')
                    faktura.drawString(x+400,y,f'{round((cenaNetto),2)}')
                    faktura.drawString(x+450,y,f'{round((cena),2)}')
                    faktura.drawString(x+490,y,f'{pakiet.cena} PLN')
                    faktura.line(15, wysokosc, 590, wysokosc)

                    podatekSuma += podatek
                    nettoSuma += cenaNetto
                    bruttoSuma += cena
                
                wysokosc -= 15
                faktura.line(15, wysokosc, 590, wysokosc)

                faktura.setFont("Verdana", 18)
                faktura.drawString(400, 320, "Podsumowanie")
                faktura.setFont("Verdana", 10)
                faktura.drawString(400, 300, f'Podatek: {round(podatekSuma,2)} PLN')
                faktura.drawString(400, 290, f'Netto: {round(nettoSuma,2)} PLN')
                faktura.drawString(400, 280, f'Brutto: {round(bruttoSuma, 2)} PLN')
                faktura.drawString(400, 270, f'Sposób płatności: przelew')
                faktura.drawString(400, 260, f'Saldo przed: {klient.stanKonta}')
                faktura.setFont("Verdana", 18)
                faktura.drawString(200, 200, f'Łączna kwota do zapłaty: {round(bruttoSuma, 2)} PLN')


                faktura.showPage()
                faktura.save()
                
                klient.stanKonta -= round(bruttoSuma, 2)
                klient.save()


            
            

            Faktura.objects.create(typ = "faktura", 
            uzytkownik = klient, nazwa=nazwa, koszt=round(bruttoSuma,2), saldoPo=klient.stanKonta, 
            faktura=f'/faktury/{nazwaPliku}.pdf', dataWystawienia=aktualny, terminPlatnosci = '2023-12-11', 
            sposobPlatnosci = 'gotowka')
            
            if klient.email:
            
                mail = klient.email
                tytul = "Faktura za usługi telekomunikacyjne"
                
                tresc = """\
                <html>
                <head></head>
                <body>
                Dzień dobry <b> %s %s ,</b> <br>
                wystawiliśmy fakturę na kwotę <b> %s <br>
                Dokument znajduje się w załączniku

                </body>
                </html>
                """ % (klient.imie, klient.nazwisko, bruttoSuma)

                wiadomosc = EmailMessage(tytul, tresc, settings.EMAIL_HOST_USER, [mail])
                wiadomosc.attach_file(f'pliki/faktury/{nazwaPliku}.pdf')
                wiadomosc.content_subtype = "html"
                wiadomosc.send()
            

                
                


    return render(request, 'finanse/finanse.html', {})   

@login_required(login_url="logowanie")
def ksiegowanie(request):
    #arkusz = request.FILES['arkusz']

    
    with io.TextIOWrapper(request.FILES["arkusz"], encoding="utf-8") as arkusz:
        platnosci = csv.DictReader(arkusz)
        aktualny = datetime.date.today()

        miesiace = {1:"STY", 2:"LUT", 3:"MAR", 4:"KWI", 5:"MAJ", 6:"CZE",7:"LIP", 8:"SIE", 9:"WRZ", 10:"PAZ", 11:"LIS", 12:"GRU"}

        for platnosc in platnosci:

            
        
            
            wynik = Faktura.objects.filter(nazwa__icontains = f'{miesiace[aktualny.month]}/{aktualny.year}/P')
            ilosc = wynik.count()

            if ilosc == 0:
                numerPlatnosci = 1
                    
            else:
                numerPlatnosci = ilosc + 1

            konto = KontoBankowe.objects.get(numerKonta = platnosc['Numer Konta'])
            klient = Klient.objects.get(id = konto.klient_id)
            
            
        
            
            klient.stanKonta += float(platnosc['Kwota'])
            klient.save()

            nazwa = f'{numerPlatnosci}/{miesiace[aktualny.month]}/{aktualny.year}/P'
            Faktura.objects.create(typ = "płatność", uzytkownik = klient, nazwa=nazwa, koszt=round(float(platnosc['Kwota']),2), saldoPo=klient.stanKonta , dataWystawienia=aktualny, notatka = platnosc['Treść przelewu'])
        


    return render(request, 'finanse/finanse.html', {})  