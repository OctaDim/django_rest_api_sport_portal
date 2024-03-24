# Generated by Django 4.2.9 on 2024-03-24 18:34

import apps.api.emotional_level.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emotional_level', '0005_alter_emotionallevel_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emotionallevel',
            name='value',
            field=models.SmallIntegerField(unique=True, verbose_name='emotional level value'),
        ),
    ]