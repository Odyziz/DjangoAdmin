# Generated by Django 3.2.8 on 2022-04-03 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('klienci', '0007_alter_klient_numergsm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='klient',
            name='email',
            field=models.EmailField(blank=True, default=1, max_length=254),
            preserve_default=False,
        ),
    ]
