# Generated by Django 3.0.7 on 2020-06-19 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bid', '0003_auto_20200618_1611'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bidpull',
            old_name='pull',
            new_name='listing',
        ),
        migrations.RenameField(
            model_name='bidpush',
            old_name='push',
            new_name='listing',
        ),
        migrations.AlterField(
            model_name='bid',
            name='comment',
            field=models.TextField(blank=True, default=''),
        ),
    ]
