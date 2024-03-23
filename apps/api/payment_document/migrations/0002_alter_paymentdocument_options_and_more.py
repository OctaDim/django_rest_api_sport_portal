# Generated by Django 4.2.9 on 2024-03-22 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_document', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentdocument',
            options={'ordering': ['name'], 'verbose_name': 'payment documents', 'verbose_name_plural': 'payment documents'},
        ),
        migrations.AlterField(
            model_name='paymentdocument',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='payment document'),
        ),
    ]