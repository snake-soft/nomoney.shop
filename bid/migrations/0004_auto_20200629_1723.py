# Generated by Django 3.0.7 on 2020-06-29 15:23

import bid.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bid', '0003_auto_20200625_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'unseen'), (10, 'seen'), (20, 'accepted'), (30, 'answered'), (40, 'rejected')], default=bid.models.StatusCode['UNSEEN']),
        ),
    ]
