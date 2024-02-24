# Generated by Django 4.2.9 on 2024-02-24 17:55

import apps.api.self_satisfaction_level.functions
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('self_satisfaction_level', '0013_remove_selfsatisfactionlevel_test_pillow_icon_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selfsatisfactionlevel',
            name='icon_link',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=100, scale=None, size=[150, 150], upload_to=apps.api.self_satisfaction_level.functions.get_image_file_name, verbose_name='self satisfaction level icon link'),
        ),
    ]