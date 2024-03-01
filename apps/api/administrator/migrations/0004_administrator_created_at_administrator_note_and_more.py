# Generated by Django 4.2.9 on 2024-02-26 18:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0003_administrator_bibliography'),
    ]

    operations = [
        migrations.AddField(
            model_name='administrator',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='administrator',
            name='note',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='note'),
        ),
        migrations.AddField(
            model_name='administrator',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated date'),
        ),
    ]
