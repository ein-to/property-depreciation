# Generated by Django 2.1.15 on 2020-05-25 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload_db', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='main',
            name='date_vvod',
        ),
        migrations.RemoveField(
            model_name='main',
            name='pur_date',
        ),
    ]