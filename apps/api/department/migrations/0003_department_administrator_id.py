# Generated by Django 4.2.9 on 2024-02-28 01:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0007_alter_administrator_options'),
        ('department', '0002_alter_department_company_id_alter_department_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='administrator_id',
            field=models.ForeignKey(default=34, on_delete=django.db.models.deletion.PROTECT, related_name='departments', to='administrator.administrator', verbose_name='department administrator'),
            preserve_default=False,
        ),
    ]