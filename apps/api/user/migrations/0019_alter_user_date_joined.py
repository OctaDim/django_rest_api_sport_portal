# Generated by Django 4.2.9 on 2024-03-05 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_alter_user_user_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(blank=True, null=True, verbose_name='joined first date'),
        ),
    ]