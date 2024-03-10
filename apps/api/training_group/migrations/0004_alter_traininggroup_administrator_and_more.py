# Generated by Django 4.2.9 on 2024-03-10 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coach', '0001_initial'),
        ('administrator', '0015_alter_administrator_bibliography_and_more'),
        ('client', '0006_alter_client_thumbnail_link'),
        ('training_group', '0003_traininggroup_client_traininggroup_coach_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traininggroup',
            name='administrator',
            field=models.ManyToManyField(blank=True, related_name='training_group', to='administrator.administrator', verbose_name='administrator'),
        ),
        migrations.AlterField(
            model_name='traininggroup',
            name='client',
            field=models.ManyToManyField(blank=True, related_name='training_group', to='client.client', verbose_name='client'),
        ),
        migrations.AlterField(
            model_name='traininggroup',
            name='coach',
            field=models.ManyToManyField(blank=True, related_name='training_group', to='coach.coach', verbose_name='coach'),
        ),
    ]