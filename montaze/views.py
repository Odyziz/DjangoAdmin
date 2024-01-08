from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Montaz
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import DodawanieNowegoMontazu
from django.http import HttpResponseRedirect
from .models import MontazHistoria
from twilio.rest import Client
from django.conf import settings
from klienci.models import Miasto


@login_required(login_url="logowanie")
def montaze(request):
    ostatni = Montaz.objects.order_by('id').last()

    paginacja = Paginator(Montaz.objects.filter(status = True),10)
    strona = request.GET.get('strona')
    montaze = paginacja.get_page(strona)
    numeracja = "i" * montaze.paginator.num_pages
    miasta = Miasto.objects.all()
    

    submitted = False
    if 'dodaj' in request.POST:
        
        
        
        form = DodawanieNowegoMontazu(request.POST)
        if form.is_valid():
            
            
            
            form.save()
            montaz = Montaz.objects.order_by('id').last()
            MontazHistoria.objects.create(uzytkownik=request.user, zmieniono="Przyjęto zamówienie", montaz = montaz)
            
          
            return HttpResponseRedirect('/montaze?submitted=True')
            


    else: 
        form = DodawanieNowegoMontazu
        if 'submitted' in request.GET:
            submitted = True   
    

    if 'archiwum' in request.POST:
        doArchiwum = Montaz.objects.get(id = request.POST['id'] )
        doArchiwum.status = False
        doArchiwum.save()


    
    return render(request, 'montaze/montaze.html', {'montaze':montaze, 'form':form, 
    'submitted':submitted, 'ostatni': ostatni, 'numeracja':numeracja, "miasta":miasta})

@login_required(login_url="logowanie")
def montaz(request, id):

    montaz = Montaz.objects.get(pk = id)
    form = DodawanieNowegoMontazu(request.POST or None, instance = montaz)
    historia = MontazHistoria.objects.all().order_by('-data')
    
    

    if 'przyciskEdytuj' in request.POST: 
        
        if form.is_valid():
            form.save()
            
            MontazHistoria.objects.create(uzytkownik=request.user, zmieniono="Zmiana danych", montaz = montaz)
            
            
            
    
    


 
    return render(request, "montaze/montaz.html", {'montaz': montaz, 'form': form, 'historia':historia})





@login_required(login_url="logowanie")
def wyslij_sms_montaz(request):   
    blad = 1
    if request.method == 'POST':
        
        try:
            
            sms = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
            numer = request.POST['telefon']
            tresc = request.POST['tresc']
            message = sms.messages.create(
                
                to=numer, 
                from_= settings.TWILIO_NUMBER,
                body=tresc)

        
            
            montaz = Montaz.objects.get(id = request.POST['id'])
            MontazHistoria.objects.create(uzytkownik=request.user, zmieniono=f'SMS na numer {numer} został wysłany', montaz = montaz)
        
        except:
            return render(request, "montaze/sms.html", {"blad":blad})
            
    
    
        
    blad -= 1
    return render(request, "montaze/sms.html", {"blad":blad})




@login_required(login_url="logowanie")
def archiwum(request):


    montaze = Montaz.objects.filter(status = False)
 

    
    
    return render(request, 'montaze/archiwum.html', {"montaze":montaze})