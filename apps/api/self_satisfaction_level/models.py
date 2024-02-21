from django.db import models
from django.utils.translation import gettext_lazy

from apps.api.messages_fields import (SATISFACTION_LEVEL,
                                      SATISFACTION_LEVELS,
                                      SATISFACTION_LEVEL_NAME,
                                      SATISFACTION_LEVEL_VALUE,
                                      SATISFACTION_LEVEL_ICON,
                                      DESCRIPTION,
                                      CREATED_AT,
                                      UPDATED_AT,
                                      CREATOR,
                                      )

from apps.api.user.models import User



class SelfSatisfactionLevel(models.Model):
    icon = models.ImageField(name="self satisfaction level icon",
                             width_field=30,
                             height_field=30,
                             blank=True, null=True,
                             verbose_name=gettext_lazy(SATISFACTION_LEVEL_ICON))

    value = models.SmallIntegerField(
                            unique=True,
                            verbose_name=gettext_lazy(SATISFACTION_LEVEL_VALUE))

    name = models.CharField(max_length=50,
                            unique=True,
                            verbose_name=gettext_lazy(SATISFACTION_LEVEL_NAME))

    description = models.TextField(max_length=300,
                                   blank=True, null=True,
                                   verbose_name=gettext_lazy(DESCRIPTION))

    created_at = models.DateTimeField(auto_now_add=True,
                                        verbose_name=gettext_lazy(CREATED_AT))

    updated_at = models.DateTimeField(auto_now=True,
                                        verbose_name=gettext_lazy(UPDATED_AT))

    creator = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                verbose_name=gettext_lazy(CREATOR))

    class Meta:
        verbose_name = gettext_lazy(SATISFACTION_LEVEL)
        verbose_name_plural = gettext_lazy(SATISFACTION_LEVELS)
        ordering = ["value"]
