from django import forms
from django.forms import ModelForm
from .models import Klient

class DodawanieNowegoKlienta(ModelForm):
    class Meta:
        model = Klient
        fields = (
            'imie',
            'nazwisko',
            'pesel',
            'seriaDowodu',
            'numerGSM',
            'numerStacjonarny',
            'email',
            'miastoZamieszkania',
            'ulicaZamieszkania',
            'numerZamieszkania',
            'numerMieszkaniaZamieszkania',
            'kodPocztowyZamieszkania',
            'wojewodztwoInstalacji',
            'powiatInstalacji',
            'gminaInstalacji',
            'miastoInstalacji',
            'ulicaInstalacji',
            'numerInstalacji',
            'numerMieszkaniaInstalacji',
            'kodPocztowyInstalacji',
            'taryfa',
            'pakiety',

        )

        labels = {
            'imie': 'Dane podstawowe',
            'nazwisko':'',
            'pesel':'',
            'seriaDowodu':'',
            'numerGSM':'Dane kontaktowe:',
            'numerStacjonarny':'',
            'email':'',
            'miastoZamieszkania':'Adres zamieszkania',
            'ulicaZamieszkania':'',
            'numerZamieszkania':'',
            'numerMieszkaniaZamieszkania':'',
            'kodPocztowyZamieszkania':'',
            'wojewodztwoInstalacji':'Adres Instalacji: Województwo',
            'powiatInstalacji': 'Powiat',
            'gminaInstalacji': 'Gmina',
            'miastoInstalacji': 'Miejsowość',
            'ulicaInstalacji': 'Ulica',
            'numerInstalacji': '',
            'numerMieszkaniaInstalacji': "",
            'kodPocztowyInstalacji': "", 
        }

        widgets = {
            'imie':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Imię'}),
            'nazwisko':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nazwisko'}),
            'pesel':forms.TextInput(attrs={'class':'form-control', 'placeholder':'PESEL'}),
            'seriaDowodu':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Seria dowodu osobistego'}),
            'numerGSM':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Numer komórkowy'}),
            'numerStacjonarny':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Numer domowy'}),
            'email':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adres email'}),
            'miastoZamieszkania':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Miejsowość'}),
            'ulicaZamieszkania':forms.TextInput(attrs={'class':"form-control", 'placeholder':'Ulica'}),
            'numerZamieszkania':forms.TextInput(attrs={'class':"form-control", 'placeholder':'Numer'}),
            'numerMieszkaniaZamieszkania':forms.TextInput(attrs={'class':"form-control", 'placeholder':'Numer mieszkania'}),
            'kodPocztowyZamieszkania':forms.TextInput(attrs={'class':"form-control", 'placeholder':'Kod pocztowy'}),
            'numerInstalacji':forms.TextInput(attrs={'class':"form-control", 'placeholder':'Numer'}),
            'numerMieszkaniaInstalacji':forms.TextInput(attrs={'class':"form-control", 'placeholder':'Numer mieszkania'}),
            'kodPocztowyInstalacji':forms.TextInput(attrs={'class':"form-control", 'placeholder':'Kod pocztowy'}),
        }

        