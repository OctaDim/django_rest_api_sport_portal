from django.db import models
# Create your models here.

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_fields import (TRAINING_GROUP,
                                                   CLIENT,
                                                   PAYMENT,
                                                   PAYMENTS,
                                                   PAYMENT_AMOUNT,
                                                   PAYMENT_REFUND,
                                                   PAYMENT_DATE,
                                                   PAYMENT_TYPE,
                                                   PAYMENT_DOCUMENT,
                                                   DESCRIPTION,
                                                   NOTE,
                                                   CREATED_AT,
                                                   UPDATED_AT,
                                                   CREATOR
                                                   )

from apps.api.user.models import User
from apps.api.training_group.models import TrainingGroup
from apps.api.client.models import Client
from apps.api.payment_type.models import PaymentType
from apps.api.payment_document.models import PaymentDocument



class GroupClientPayment(models.Model):
    training_group = models.ForeignKey(
                        TrainingGroup,
                        on_delete=models.PROTECT,
                        related_name="group_client_payment",
                        verbose_name=gettext_lazy(TRAINING_GROUP))

    client = models.ForeignKey(Client,
                        on_delete=models.PROTECT,
                        related_name="group_client_payment",
                        verbose_name=gettext_lazy(CLIENT))

    payment_amount = models.FloatField(
                            blank=True, null=True,
                            verbose_name=gettext_lazy(PAYMENT_AMOUNT))

    refund_amount = models.FloatField(
                            blank=True, null=True,
                            verbose_name=gettext_lazy(PAYMENT_REFUND))

    payment_date = models.DateField(verbose_name=gettext_lazy(PAYMENT_DATE))

    payment_type = models.ForeignKey(
                        PaymentType,
                        on_delete=models.PROTECT,
                        related_name="group_client_payment",
                        verbose_name=gettext_lazy(PAYMENT_TYPE))

    payment_document = models.ForeignKey(
                        PaymentDocument,
                        on_delete=models.PROTECT,
                        related_name="group_client_payment",
                        verbose_name=gettext_lazy(PAYMENT_DOCUMENT))

    description = models.TextField(max_length=300,
                                   blank=True, null=True,
                                   verbose_name=gettext_lazy(DESCRIPTION))

    note = models.CharField(max_length=150,
                            blank=True, null=True,
                            verbose_name=gettext_lazy(NOTE))

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=gettext_lazy(CREATED_AT))

    updated_at = models.DateTimeField(auto_now=True,
                                        verbose_name=gettext_lazy(UPDATED_AT))

    creator = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                related_name='group_client_payment',
                                verbose_name=gettext_lazy(CREATOR))

    class Meta:
        verbose_name = gettext_lazy(PAYMENT)
        verbose_name_plural = gettext_lazy(PAYMENTS)
        ordering = ["payment_date"]

    def __str__(self):
        return (f"{self.payment_date}: "
                f"[+{self.payment_amount}]"
                f"[-self.refund_amount]")
