# Generated by Django 4.2.9 on 2024-02-28 02:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('self_satisfaction_level', '0014_alter_selfsatisfactionlevel_icon_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selfsatisfactionlevel',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='self_satisfaction_level', to=settings.AUTH_USER_MODEL, verbose_name='creator'),
        ),
    ]
