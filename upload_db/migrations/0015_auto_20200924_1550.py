# Generated by Django 3.0.6 on 2020-09-24 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload_db', '0014_employees_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='employees_id',
            new_name='employee_id',
        ),
    ]
