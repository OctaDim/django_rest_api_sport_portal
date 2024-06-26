# Generated by Django 4.2.9 on 2024-03-22 18:25

import apps.api.utils.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment_document', '0002_alter_paymentdocument_options_and_more'),
        ('payment_type', '0002_alter_paymenttype_options_alter_paymenttype_name'),
        ('group_client_payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupclientpayment',
            options={'ordering': ['payment_date'], 'verbose_name': 'payment', 'verbose_name_plural': 'payments'},
        ),
        migrations.AlterField(
            model_name='groupclientpayment',
            name='payment_amount',
            field=models.FloatField(blank=True, null=True, validators=[apps.api.utils.utils.number_or_str_to_abs_float], verbose_name='payment amount'),
        ),
        migrations.AlterField(
            model_name='groupclientpayment',
            name='payment_date',
            field=models.DateField(verbose_name='payment date'),
        ),
        migrations.AlterField(
            model_name='groupclientpayment',
            name='payment_document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='group_client_payment', to='payment_document.paymentdocument', verbose_name='payment document'),
        ),
        migrations.AlterField(
            model_name='groupclientpayment',
            name='payment_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='group_client_payment', to='payment_type.paymenttype', verbose_name='payment type'),
        ),
        migrations.AlterField(
            model_name='groupclientpayment',
            name='refund_amount',
            field=models.FloatField(blank=True, null=True, validators=[apps.api.utils.utils.number_or_str_to_abs_float], verbose_name='payment refund'),
        ),
    ]
