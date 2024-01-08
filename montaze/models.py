from django.db import models
from klienci.models import Miasto, Ulica
from django.contrib.auth.models import User



class Montaz(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    miasto = models.ForeignKey(Miasto, on_delete=models.CASCADE)
    ulica = models.ForeignKey(Ulica, on_delete=models.CASCADE)
    numerDomu = models.CharField(max_length=10)
    numerMieszkania = models.CharField(max_length=4, blank=True, null=True)
    informacjaBiuro = models.TextField(max_length=50, blank=True)
    informacjaMontaz = models.TextField(max_length=50, blank=True)
    telefon = models.CharField(max_length=15)
    alternatywny = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Montaż"
        verbose_name_plural = "Montaże"


class MontazHistoria(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    zmieniono = models.CharField(max_length=100)
    montaz = models.ForeignKey(Montaz, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Historia montażu"
        verbose_name_plural = "Historia montaży"