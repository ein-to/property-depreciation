# Generated by Django 3.0.6 on 2020-07-24 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload_db', '0008_company_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company_id',
            name='company_id',
        ),
    ]
