# Generated by Django 4.2.9 on 2024-02-13 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_managers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['email', 'username', 'nickname'], 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
