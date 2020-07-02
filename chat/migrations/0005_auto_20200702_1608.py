# Generated by Django 3.0.7 on 2020-07-02 14:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0004_userchat'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserChat',
        ),
    ]
