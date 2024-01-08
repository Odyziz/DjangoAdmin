# Generated by Django 3.2.8 on 2022-05-02 15:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('klienci', '0011_alter_klient_email'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Montaz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imie', models.CharField(max_length=50)),
                ('nazwisko', models.CharField(max_length=50)),
                ('numerDomu', models.CharField(max_length=10)),
                ('numerMieszkania', models.CharField(blank=True, max_length=4, null=True)),
                ('informacjaBiuro', models.TextField(blank=True, max_length=50)),
                ('informacjaMontaz', models.TextField(blank=True, max_length=50)),
                ('telefon', models.CharField(max_length=15)),
                ('alternatywny', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('miasto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='klienci.miasto')),
                ('ulica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='klienci.ulica')),
            ],
        ),
        migrations.CreateModel(
            name='MontazHistoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('zmieniono', models.CharField(max_length=100)),
                ('montaz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='montaze.montaz')),
                ('uzytkownik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
