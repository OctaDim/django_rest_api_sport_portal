from django.db import models
from django.utils.translation import gettext_lazy

from apps.api.messages_fields import (CLIENT_STATUS,
                                      CLIENT_STATUSES,
                                      CREATED_AT,
                                      UPDATED_AT,
                                      CREATOR,
                                      )

from apps.api.user.models import User



class ClientStatus(models.Model):
    name = models.CharField(max_length=30,
                            verbose_name=gettext_lazy(CLIENT_STATUS))

    created_at = models.DateTimeField(auto_now_add=True,
                                        verbose_name=gettext_lazy(CREATED_AT))

    updated_at = models.DateTimeField(auto_now=True,
                                        verbose_name=gettext_lazy(UPDATED_AT))

    creator = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                verbose_name=gettext_lazy(CREATOR))

    class Meta:
        verbose_name = gettext_lazy(CLIENT_STATUS)
        verbose_name_plural = gettext_lazy(CLIENT_STATUSES)
        ordering = ["name"]
