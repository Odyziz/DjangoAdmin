# Generated by Django 3.2.8 on 2022-04-03 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('klienci', '0006_alter_klient_numerstacjonarny'),
    ]

    operations = [
        migrations.AlterField(
            model_name='klient',
            name='numerGSM',
            field=models.CharField(blank=True, default=1, max_length=20),
            preserve_default=False,
        ),
    ]
