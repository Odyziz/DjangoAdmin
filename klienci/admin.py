from django.contrib import admin
from . import models

admin.site.register(models.Klient)
admin.site.register(models.Wojewodztwo)
admin.site.register(models.Powiat)
admin.site.register(models.Gmina)
admin.site.register(models.Miasto)
admin.site.register(models.Ulica)
admin.site.register(models.Skan)
admin.site.register(models.Faktura)
admin.site.register(models.KontoBankowe)
admin.site.register(models.Umowa)

@admin.register(models.KlientHistoria)
class KlientHistoriaAdmin(admin.ModelAdmin):
    
    fields= [
        'uzytkownik',
        'data',
        'zmieniono',
        'klient',
        ]
    
    readonly_fields= ['uzytkownik','data','zmieniono','klient']


