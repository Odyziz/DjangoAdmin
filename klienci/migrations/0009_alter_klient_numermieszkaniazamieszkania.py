# Generated by Django 3.2.8 on 2022-04-03 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('klienci', '0008_alter_klient_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='klient',
            name='numerMieszkaniaZamieszkania',
            field=models.CharField(blank=True, default=1, max_length=50),
            preserve_default=False,
        ),
    ]
