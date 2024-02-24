# Generated by Django 4.2.9 on 2024-02-21 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SelfSatisfactionLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('self satisfaction level icon', models.ImageField(blank=True, height_field=30, null=True, upload_to='', verbose_name='self satisfaction level icon', width_field=30)),
                ('value', models.SmallIntegerField(unique=True, verbose_name='self satisfaction level value')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='self satisfaction level name')),
                ('description', models.TextField(blank=True, max_length=300, null=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated date')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
            ],
            options={
                'verbose_name': 'self satisfaction level',
                'verbose_name_plural': 'self satisfaction levels',
                'ordering': ['value'],
            },
        ),
    ]