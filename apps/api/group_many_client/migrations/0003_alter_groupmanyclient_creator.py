# Generated by Django 4.2.9 on 2024-03-20 02:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group_many_client', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmanyclient',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='group_many_client', to=settings.AUTH_USER_MODEL, verbose_name='creator'),
        ),
    ]