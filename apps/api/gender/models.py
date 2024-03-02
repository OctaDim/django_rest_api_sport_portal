from django.db import models
from django.utils.translation import gettext_lazy

from apps.api.messages_fields import (GENDER,
                                      GENDERS,
                                      CREATED_AT,
                                      UPDATED_AT,
                                      CREATOR,
                                      )

from apps.api.user.models import User



class Gender(models.Model):
    name = models.CharField(max_length=30,
                            unique=True,
                            verbose_name=gettext_lazy(GENDER))

    created_at = models.DateTimeField(auto_now_add=True,
                                        verbose_name=gettext_lazy(CREATED_AT))

    updated_at = models.DateTimeField(auto_now=True,
                                        verbose_name=gettext_lazy(UPDATED_AT))

    creator = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                related_name='gender',
                                verbose_name=gettext_lazy(CREATOR))

    class Meta:
        verbose_name = gettext_lazy(GENDER)
        verbose_name_plural = gettext_lazy(GENDERS)
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
