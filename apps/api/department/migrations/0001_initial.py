# Generated by Django 4.2.9 on 2024-02-21 01:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='company department')),
                ('address', models.CharField(max_length=300, verbose_name='Address')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='description')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated date')),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='departments', to='company.company', verbose_name='company')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
            ],
            options={
                'verbose_name': 'department',
                'verbose_name_plural': 'departments',
                'ordering': ['name', 'is_active'],
            },
        ),
    ]
