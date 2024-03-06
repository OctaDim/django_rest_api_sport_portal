# Generated by Django 4.2.9 on 2024-02-28 02:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrator', '0008_alter_administrator_creator'),
        ('department', '0003_department_administrator_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='company_id',
        ),
        migrations.AddField(
            model_name='department',
            name='company',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, related_name='department', to='company.company', verbose_name='department company'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='department',
            name='administrator_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='department', to='administrator.administrator', verbose_name='department administrator'),
        ),
        migrations.AlterField(
            model_name='department',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='department', to=settings.AUTH_USER_MODEL, verbose_name='creator'),
        ),
    ]