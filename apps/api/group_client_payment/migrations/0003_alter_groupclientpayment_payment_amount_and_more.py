# Generated by Django 4.2.9 on 2024-03-11 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_client_payment', '0002_groupclientpayment_delete_traininggroupclientpayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupclientpayment',
            name='payment_amount',
            field=models.FloatField(blank=True, null=True, verbose_name='Payment amount'),
        ),
        migrations.AlterField(
            model_name='groupclientpayment',
            name='payment_date',
            field=models.DateField(verbose_name='Payment date'),
        ),
        migrations.AlterField(
            model_name='groupclientpayment',
            name='refund_amount',
            field=models.FloatField(blank=True, null=True, verbose_name='Payment refund'),
        ),
    ]
