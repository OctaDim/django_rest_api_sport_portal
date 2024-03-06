# Generated by Django 4.2.9 on 2024-02-28 02:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client_status', '0002_clientstatus_description_alter_clientstatus_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientstatus',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client_status', to=settings.AUTH_USER_MODEL, verbose_name='creator'),
        ),
    ]