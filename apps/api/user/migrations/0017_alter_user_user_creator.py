# Generated by Django 4.2.9 on 2024-03-04 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_rename_creator_user_user_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='user creator'),
        ),
    ]
