# Generated by Django 3.2.8 on 2022-03-21 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zarzadzanie', '0002_remove_taryfa_podatek'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taryfa',
            options={},
        ),
        migrations.AddField(
            model_name='taryfa',
            name='podatek',
            field=models.FloatField(default=23),
            preserve_default=False,
        ),
    ]