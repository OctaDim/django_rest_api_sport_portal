# Generated by Django 4.2.9 on 2024-03-20 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_year', '0003_alter_trainingyear_options_alter_trainingyear_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingyear',
            name='finish_date',
            field=models.DateField(blank=True, null=True, verbose_name='finish date'),
        ),
        migrations.AlterField(
            model_name='trainingyear',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='start date'),
        ),
    ]