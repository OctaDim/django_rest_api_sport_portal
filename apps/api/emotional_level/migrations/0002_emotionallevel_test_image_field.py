# Generated by Django 4.2.9 on 2024-02-24 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emotional_level', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emotionallevel',
            name='test_image_field',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
