# Generated by Django 4.2.9 on 2024-03-04 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0005_rename_administrator_id_department_administrator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='address',
            field=models.CharField(max_length=300, verbose_name='address'),
        ),
    ]