# Generated by Django 3.2.8 on 2022-04-02 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0005_zgloszenie_zamkniete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zgloszenie',
            name='zamkniete',
        ),
    ]
