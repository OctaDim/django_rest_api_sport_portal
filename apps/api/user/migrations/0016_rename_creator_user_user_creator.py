# Generated by Django 4.2.9 on 2024-03-03 02:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_remove_user_creator_user_user_creator_delete_creator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='creator',
            new_name='user_creator',
        ),
    ]