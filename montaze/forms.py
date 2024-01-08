from django import forms
from django.forms import ModelForm

from .models import Montaz

class DodawanieNowegoMontazu(ModelForm):
    class Meta:
        model = Montaz
        fields = (
            'imie',
            'nazwisko',
            'miasto',
            'ulica',
            'numerDomu',
            'numerMieszkania',
            'informacjaBiuro',
            'informacjaMontaz',
            'telefon',
            'alternatywny',
            'email',
            

        )


    