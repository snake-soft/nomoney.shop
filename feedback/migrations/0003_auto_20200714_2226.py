# Generated by Django 3.0.7 on 2020-07-14 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deal', '0005_auto_20200714_2226'),
        ('feedback', '0002_auto_20200714_1425'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pushfeedback',
            options={'verbose_name': 'pushfeedback', 'verbose_name_plural': 'pushfeedbacks'},
        ),
        migrations.AlterModelOptions(
            name='userfeedback',
            options={'verbose_name': 'userfeedback', 'verbose_name_plural': 'userfeedbacks'},
        ),
        migrations.AlterField(
            model_name='pushfeedback',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='pushfeedback',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='creator'),
        ),
        migrations.AlterField(
            model_name='pushfeedback',
            name='deal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deal.Deal', verbose_name='deal'),
        ),
        migrations.AlterField(
            model_name='pushfeedback',
            name='score',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='score'),
        ),
        migrations.AlterField(
            model_name='pushfeedback',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'request'), (100, 'sent'), (110, 'canceled')], default=0, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='pushfeedback',
            name='subject',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='subject'),
        ),
        migrations.AlterField(
            model_name='pushfeedback',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='creator'),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='deal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deal.Deal', verbose_name='deal'),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='score',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='score'),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'request'), (100, 'sent'), (110, 'canceled')], default=0, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='subject',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='subject'),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_for', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
