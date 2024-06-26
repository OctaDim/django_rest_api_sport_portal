# Generated by Django 4.2.9 on 2024-03-12 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('department', '0010_alter_department_options'),
        ('coach', '0001_initial'),
        ('group_many_client', '0001_initial'),
        ('administrator', '0015_alter_administrator_bibliography_and_more'),
        ('training_year', '0003_alter_trainingyear_options_alter_trainingyear_name'),
        ('client', '0006_alter_client_thumbnail_link'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_group_code', models.CharField(max_length=50, unique=True, verbose_name='training group code')),
                ('training_group_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='training group name')),
                ('description', models.TextField(blank=True, max_length=300, null=True, verbose_name='description')),
                ('note', models.CharField(blank=True, max_length=150, null=True, verbose_name='note')),
                ('start_date', models.DateField(verbose_name='start date')),
                ('finish_date', models.DateField(verbose_name='finish date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated date')),
                ('administrator', models.ManyToManyField(blank=True, related_name='training_group', to='administrator.administrator', verbose_name='administrator')),
                ('client', models.ManyToManyField(blank=True, related_name='training_group', through='group_many_client.GroupManyClient', to='client.client', verbose_name='client')),
                ('coach', models.ManyToManyField(blank=True, related_name='training_group', to='coach.coach', verbose_name='coach')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='training_group', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='training_group', to='department.department', verbose_name='department')),
                ('training_year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='training_group', to='training_year.trainingyear', verbose_name='training year (period)')),
            ],
            options={
                'verbose_name': 'training group',
                'verbose_name_plural': 'training groups',
                'ordering': ['training_group_code', 'training_group_name'],
            },
        ),
    ]
