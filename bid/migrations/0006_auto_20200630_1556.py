# Generated by Django 3.0.7 on 2020-06-30 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0002_auto_20200625_2315'),
        ('bid', '0005_auto_20200629_1919'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BidPull',
            new_name='BidPosition',
        ),
        migrations.RemoveField(
            model_name='bidposition',
            name='listing',
        ),
        migrations.AddField(
            model_name='bidposition',
            name='push',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='listing.Push'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='BidPush',
        ),
    ]