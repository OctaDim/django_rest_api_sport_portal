# Generated by Django 4.2.9 on 2024-02-22 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('self_satisfaction_level', '0002_remove_selfsatisfactionlevel_self_satisfaction_level_icon_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selfsatisfactionlevel',
            name='icon',
        ),
        migrations.AddField(
            model_name='selfsatisfactionlevel',
            name='self satisfaction level icon',
            field=models.ImageField(blank=True, height_field=30, null=True, upload_to='', verbose_name='self satisfaction level icon', width_field=30),
        ),
    ]
