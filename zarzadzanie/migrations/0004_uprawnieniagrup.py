# Generated by Django 3.2.8 on 2022-04-12 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('zarzadzanie', '0003_auto_20220321_0235'),
    ]

    operations = [
        migrations.CreateModel(
            name='UprawnieniaGrup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modulFinanse', models.BooleanField()),
                ('modulHelpdesk', models.BooleanField()),
                ('modulKlienci', models.BooleanField()),
                ('modulMontaze', models.BooleanField()),
                ('modulZardzanie', models.BooleanField()),
                ('grupa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
    ]
