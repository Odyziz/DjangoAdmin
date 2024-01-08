from django.db import models
from django.contrib.auth.models import Group


class Taryfa(models.Model):
    nazwaTaryfy = models.CharField(max_length=100)
    pobieranie = models.CharField(max_length=20)
    wysylanie = models.CharField(max_length=20)
    cena = models.FloatField()
    podatek = models.FloatField()
    
    def __str__(self):
        return f'{self.nazwaTaryfy}'
    
    class Meta:
        verbose_name = "Taryfa"
        verbose_name_plural = "Taryfy"

    
class PakietDodatkowy(models.Model):
    nazwaPakietu = models.CharField(max_length=100)
    cena = models.FloatField()
    podatek = models.FloatField()
    
    def __str__(self):
        return self.nazwaPakietu

    class Meta:
        verbose_name = "Pakiet dodatkowy"
        verbose_name_plural = "Pakiety dodatkowe"
