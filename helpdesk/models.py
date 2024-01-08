from django.db import models
from klienci.models import Klient
from django.contrib.auth.models import User

class Zgloszenie(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    temat = models.CharField(max_length=100)
    tresc = models.TextField(max_length=500, blank=True)
    dataUtworzenia = models.DateTimeField(auto_now_add=True)
    statusRozwiazany = models.BooleanField(default=False)
    zalacznik = models.FileField(upload_to="helpdesk", blank=True, null=True)

    def __str__(self):
        return f'Zgłoszenie numer {self.pk} użytkownika ({self.klient.pk}) {self.klient}'

    class Meta:
        verbose_name = "Zgłoszenie"
        verbose_name_plural = "Zgłoszenia"
    

class ZgloszenieOdpowiedzi(models.Model):
    zgloszenie = models.ForeignKey(Zgloszenie, on_delete=models.CASCADE)
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE, blank=True, null=True)
    tresc = models.TextField(max_length=500, blank=True)
    dataUtworzenia = models.DateTimeField(auto_now_add=True)
    zalacznik = models.FileField(upload_to="helpdesk", blank=True, null=True)


        
    def __str__(self):
        return f'Odpowiedź do zgłoszenia numer {self.zgloszenie.pk}'


    class Meta:
        verbose_name = "Odpowiedź"
        verbose_name_plural = "Odpowiedzi"