# Generated by Django 3.1.3 on 2021-08-02 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_db', '0029_history_item_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='history_item',
            name='invoice_number',
            field=models.IntegerField(null=True),
        ),
    ]