# Generated by Django 3.2.8 on 2022-03-25 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('klienci', '0003_umowa'),
    ]

    operations = [
        migrations.AddField(
            model_name='umowa',
            name='umowa',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]