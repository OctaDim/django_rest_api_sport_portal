# Generated by Django 4.2.9 on 2024-03-08 00:22

import apps.api.coach.utils
import apps.api.coach.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gender', '0004_alter_gender_options_alter_gender_name'),
        ('country', '0004_alter_country_creator'),
        ('coach_speciality', '0003_alter_coachspeciality_creator'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail_link', models.ImageField(blank=True, null=True, upload_to=apps.api.coach.utils.get_image_file_name, validators=[apps.api.coach.validators.validate_image_size], verbose_name='avatar thumbnail link')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='last name')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='phone')),
                ('address', models.TextField(blank=True, max_length=500, null=True, verbose_name='address')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='birth date')),
                ('bibliography', models.TextField(blank=True, max_length=500, null=True, verbose_name='bibliography')),
                ('note', models.CharField(blank=True, max_length=150, null=True, verbose_name='note')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated date')),
                ('coach_creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='coaches', to=settings.AUTH_USER_MODEL, verbose_name='coach creator')),
                ('coach_speciality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='coach', to='coach_speciality.coachspeciality', verbose_name='coach speciality')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='coach', to='country.country', verbose_name='country')),
                ('gender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='coach', to='gender.gender', verbose_name='Gender')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='coach', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'coach',
                'verbose_name_plural': 'coaches',
                'ordering': ['user__email', 'user__username', 'user__nickname'],
            },
        ),
    ]
