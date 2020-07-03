# Generated by Django 3.0.7 on 2020-07-03 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('listing', '0001_initial'),
        ('bid', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidposition',
            name='push',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.Push'),
        ),
        migrations.AddField(
            model_name='bidposition',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.Unit'),
        ),
    ]
