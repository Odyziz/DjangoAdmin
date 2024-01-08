# Generated by Django 3.2.8 on 2022-03-30 23:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('klienci', '0004_umowa_umowa'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('helpdesk', '0003_auto_20220330_0159'),
    ]

    operations = [
        migrations.AddField(
            model_name='zgloszenieodpowiedzi',
            name='klient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='klienci.klient'),
        ),
        migrations.AlterField(
            model_name='zgloszenieodpowiedzi',
            name='uzytkownik',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
