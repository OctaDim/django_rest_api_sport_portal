# Generated by Django 4.2.9 on 2024-03-05 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_alter_user_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, default="2024-03-04 22:14:28.809589 +00:00", verbose_name='joined first date'),
            preserve_default=False,
        ),
    ]