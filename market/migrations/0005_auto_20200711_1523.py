# Generated by Django 3.0.7 on 2020-07-11 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_auto_20200711_1403'),
    ]

    operations = [
        migrations.RenameField(
            model_name='market',
            old_name='users',
            new_name='_users',
        ),
    ]
