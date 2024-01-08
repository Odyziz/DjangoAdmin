from django.forms import ModelForm

from .models import Taryfa, PakietDodatkowy

class DodawanieNowejTaryfy(ModelForm):
    class Meta:
        model = Taryfa
        fields = (
        'nazwaTaryfy', 
        'pobieranie', 
        'wysylanie',
        'cena',
        'podatek'
        
        )


