# Generated by Django 4.2.9 on 2024-02-24 17:35

import apps.api.emotional_level.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmotionalLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon_link', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=100, scale=None, size=[150, 150], upload_to=apps.api.emotional_level.utils.get_image_file_name, verbose_name='emotional level icon')),
                ('value', models.SmallIntegerField(unique=True, verbose_name='emotional level value')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='emotional level name')),
                ('description', models.TextField(blank=True, max_length=300, null=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated date')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
            ],
            options={
                'verbose_name': 'emotional level',
                'verbose_name_plural': 'emotional levels',
                'ordering': ['value'],
            },
        ),
    ]
