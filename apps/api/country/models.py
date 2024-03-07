from django.db import models
from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_fields import (COUNTRY,
                                                   COUNTRIES,
                                                   DESCRIPTION,
                                                   CREATED_AT,
                                                   UPDATED_AT,
                                                   CREATOR,
                                                   )

from apps.api.user.models import User



class Country(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name=gettext_lazy(COUNTRY))

    description = models.TextField(max_length=500,
                                   blank=True, null=True,
                                   verbose_name=gettext_lazy(DESCRIPTION))

    created_at = models.DateTimeField(auto_now_add=True,
                                        verbose_name=gettext_lazy(CREATED_AT))

    updated_at = models.DateTimeField(auto_now=True,
                                        verbose_name=gettext_lazy(UPDATED_AT))

    creator = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                related_name="country",
                                verbose_name=gettext_lazy(CREATOR))

    class Meta:
        verbose_name = gettext_lazy(COUNTRY)
        verbose_name_plural = gettext_lazy(COUNTRIES)
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
