# Generated by Django 4.2.9 on 2024-03-19 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_group', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='traininggroup',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
    ]