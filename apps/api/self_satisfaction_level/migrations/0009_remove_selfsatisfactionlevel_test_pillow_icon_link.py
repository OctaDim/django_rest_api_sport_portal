# Generated by Django 4.2.9 on 2024-02-23 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('self_satisfaction_level', '0008_selfsatisfactionlevel_test_pillow_icon_link_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selfsatisfactionlevel',
            name='test_pillow_icon_link',
        ),
    ]
