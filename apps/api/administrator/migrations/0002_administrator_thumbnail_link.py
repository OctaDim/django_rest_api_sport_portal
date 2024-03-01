# Generated by Django 4.2.9 on 2024-02-26 18:50

import apps.api.administrator.utils
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='administrator',
            name='thumbnail_link',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=100, scale=None, size=[150, 150], upload_to=apps.api.administrator.utils.get_image_file_name, verbose_name='Avatar thumbnail link'),
        ),
    ]
