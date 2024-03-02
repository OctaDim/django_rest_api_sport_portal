from django.db import models
from django.utils.translation import gettext_lazy

from apps.api.messages_fields import (CLIENT_STATUS,
                                      CLIENT_STATUSES,
                                      DESCRIPTION,
                                      CREATED_AT,
                                      UPDATED_AT,
                                      CREATOR,
                                      )

from apps.api.user.models import User



class ClientStatus(models.Model):
    name = models.CharField(max_length=50,
                            unique=True,
                            verbose_name=gettext_lazy(CLIENT_STATUS))

    description = models.TextField(max_length=300,
                                   blank=True, null=True,
                                   verbose_name=gettext_lazy(DESCRIPTION))

    created_at = models.DateTimeField(auto_now_add=True,
                                        verbose_name=gettext_lazy(CREATED_AT))

    updated_at = models.DateTimeField(auto_now=True,
                                        verbose_name=gettext_lazy(UPDATED_AT))

    creator = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                related_name='client_status',
                                verbose_name=gettext_lazy(CREATOR))

    class Meta:
        verbose_name = gettext_lazy(CLIENT_STATUS)
        verbose_name_plural = gettext_lazy(CLIENT_STATUSES)
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
