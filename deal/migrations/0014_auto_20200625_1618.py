# Generated by Django 3.0.7 on 2020-06-25 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deal', '0013_auto_20200625_1604'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deal',
            old_name='user',
            new_name='user1',
        ),
        migrations.RenameField(
            model_name='deal',
            old_name='partner',
            new_name='user2',
        ),
    ]
