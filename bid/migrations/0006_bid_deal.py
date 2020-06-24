# Generated by Django 3.0.7 on 2020-06-23 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deal', '0006_auto_20200623_2200'),
        ('bid', '0005_remove_bid_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='deal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='deal.Deal'),
            preserve_default=False,
        ),
    ]
