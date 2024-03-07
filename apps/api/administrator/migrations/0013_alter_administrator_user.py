# Generated by Django 4.2.9 on 2024-03-07 08:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrator', '0012_alter_administrator_thumbnail_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrator',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='administrator', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
