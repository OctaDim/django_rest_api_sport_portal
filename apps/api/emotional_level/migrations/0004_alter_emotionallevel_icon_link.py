# Generated by Django 4.2.9 on 2024-02-24 17:55

import apps.api.emotional_level.functions
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('emotional_level', '0003_remove_emotionallevel_test_image_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emotionallevel',
            name='icon_link',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=100, scale=None, size=[150, 150], upload_to=apps.api.emotional_level.functions.get_image_file_name, verbose_name='emotional level icon link'),
        ),
    ]