from mimetypes import init
from django.db import models
from django.contrib.auth.models import User
from zarzadzanie.models import PakietDodatkowy, Taryfa

class Wojewodztwo(models.Model):
    nazwaWojewodztwa = models.CharField(max_length=50)

    def __str__(self):
        return self.nazwaWojewodztwa

    class Meta:
        verbose_name = "Województwo"
        verbose_name_plural = "Województwa"

class Powiat(models.Model):
    wojewodztwo = models.ForeignKey(Wojewodztwo, on_delete=models.CASCADE)
    nazwaPowiatu = models.CharField(max_length=50)

    def __str__(self):
        return self.nazwaPowiatu

    class Meta:
        verbose_name = "Powiat"
        verbose_name_plural = "Powiaty"

class Gmina(models.Model):
    powiat = models.ForeignKey(Powiat, on_delete=models.CASCADE)
    nazwaGminy = models.CharField(max_length=50)

    def __str__(self):
        return self.nazwaGminy 
    
    class Meta:
        verbose_name = "Gmina"
        verbose_name_plural = "Gminy"


class Miasto(models.Model):
    gmina = models.ForeignKey(Gmina, on_delete=models.CASCADE)
    nazwaMiasta = models.CharField(max_length=50)

    def __str__(self):
        return self.nazwaMiasta

    class Meta:
        verbose_name = "Miasto"
        verbose_name_plural = "Miasta"

class Ulica(models.Model):
    miasto = models.ForeignKey(Miasto, on_delete=models.CASCADE)
    nazwaUlicy = models.CharField(max_length=50)

    def __str__(self):
        return self.nazwaUlicy
    
    class Meta:
        verbose_name = "Ulica"
        verbose_name_plural = "Ulice"






class Klient(models.Model):

    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    pesel = models.CharField(max_length=11)
    seriaDowodu = models.CharField(max_length=9)
    aktywny = models.BooleanField(default=True)
    numerGSM = models.CharField(max_length=20, blank=True)
    numerStacjonarny = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True, null=True)
    miastoZamieszkania = models.CharField(max_length=50)
    ulicaZamieszkania = models.CharField(max_length=50)
    numerZamieszkania = models.CharField(max_length=50)
    numerMieszkaniaZamieszkania = models.CharField(max_length=50,blank=True)
    kodPocztowyZamieszkania = models.CharField(max_length=6)
    wojewodztwoInstalacji = models.ForeignKey(Wojewodztwo, on_delete=models.CASCADE)
    powiatInstalacji = models.ForeignKey(Powiat, on_delete=models.CASCADE)
    gminaInstalacji = models.ForeignKey(Gmina, on_delete=models.CASCADE)
    miastoInstalacji = models.ForeignKey(Miasto, on_delete=models.CASCADE)
    ulicaInstalacji = models.ForeignKey(Ulica, on_delete=models.CASCADE)
    numerInstalacji = models.CharField(max_length=50)
    numerMieszkaniaInstalacji = models.CharField(max_length=50, blank=True)
    kodPocztowyInstalacji = models.CharField(max_length=6)
    uzytkownik = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    stanKonta = models.FloatField(default=0)
    taryfa = models.ForeignKey(Taryfa, on_delete=models.CASCADE, blank=True, null=True)
    pakiety = models.ManyToManyField(PakietDodatkowy, blank=True,)

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'

    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klienci"


class Skan(models.Model):
    nazwaSkanu = models.CharField(max_length=50)
    skan = models.FileField(upload_to="skany", blank=True, null=True)
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)

    def __str__(self):
        return self.nazwaSkanu

    class Meta:
        verbose_name = "Skan"
        verbose_name_plural = "Skany"

class KlientHistoria(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    zmieniono = models.CharField(max_length=100)
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Historia klienta"
        verbose_name_plural = "Historia klientów"

class Faktura(models.Model):
    uzytkownik = models.ForeignKey(Klient, on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=100)
    typ = models.CharField(max_length=100)
    koszt = models.FloatField()
    saldoPo = models.FloatField()
    faktura = models.FileField(blank=True, null=True)
    dataWystawienia = models.DateField(blank=True)
    terminPlatnosci = models.DateField(blank=True, null=True)
    sposobPlatnosci = models.CharField(max_length=100, blank=True)
    dataDodania = models.DateTimeField(auto_now_add=True)
    notatka = models.TextField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Faktura"
        verbose_name_plural = "Faktury"

    def __str__(self):
        return self.nazwa



class KontoBankowe(models.Model):
    numerKonta = models.CharField(max_length=26)
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE, blank=True, default=None, null=True)

    class Meta:
        verbose_name = "Konto bankowe"
        verbose_name_plural = "Konta bankowe"



class Umowa(models.Model):
    uzytkownik = models.ForeignKey(Klient, on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=100)
    dataOd = models.DateField(blank=True)
    dataDo = models.DateField(blank=True) 
    dataDodania = models.DateTimeField(auto_now_add=True)
    umowa = models.FileField(blank=True, null=True)
    czyPodpisana = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Umowa"
        verbose_name_plural = "Umowy"

    def __str__(self):
        return self.nazwa