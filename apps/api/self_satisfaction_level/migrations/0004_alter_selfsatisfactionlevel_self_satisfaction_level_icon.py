# Generated by Django 4.2.9 on 2024-02-22 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('self_satisfaction_level', '0003_remove_selfsatisfactionlevel_icon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selfsatisfactionlevel',
            name='self satisfaction level icon',
            field=models.ImageField(blank=True, null=True, upload_to='api/self_satisfaction_level', verbose_name='self satisfaction level icon'),
        ),
    ]
