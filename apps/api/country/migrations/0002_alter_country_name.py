# Generated by Django 4.2.9 on 2024-02-21 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='country from'),
        ),
    ]
