from django.db import models
from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_fields import (TRAINING_YEAR,
                                                   TRAINING_YEARS,
                                                   TRAINING_YEAR_NAME,
                                                   DESCRIPTION,
                                                   START_DATE,
                                                   FINISH_DATE,
                                                   CREATED_AT,
                                                   UPDATED_AT,
                                                   CREATOR,
                                                   )

from apps.api.user.models import User



class TrainingYear(models.Model):
    name = models.CharField(max_length=50,
                            unique=True,
                            verbose_name=gettext_lazy(TRAINING_YEAR_NAME))

    description = models.TextField(max_length=300,
                                   blank=True, null=True,
                                   verbose_name=gettext_lazy(DESCRIPTION))

    start_date = models.DateField(blank=True, null=True,
                                      verbose_name=gettext_lazy(START_DATE))

    finish_date = models.DateField(blank=True, null=True,
                                        verbose_name=gettext_lazy(FINISH_DATE))

    created_at = models.DateTimeField(auto_now_add=True,
                                        verbose_name=gettext_lazy(CREATED_AT))

    updated_at = models.DateTimeField(auto_now=True,
                                        verbose_name=gettext_lazy(UPDATED_AT))

    creator = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                related_name="training_year",
                                verbose_name=gettext_lazy(CREATOR))

    class Meta:
        verbose_name = gettext_lazy(TRAINING_YEAR)
        verbose_name_plural = gettext_lazy(TRAINING_YEARS)
        ordering = ["name"]


    def __str__(self):
        return self.__get_training_year_str_and_full_name()


    @property
    def full_name(self):
        return self.__get_training_year_str_and_full_name()


    def __get_training_year_str_and_full_name(self):
        start_date = (lambda s: s if s else "")(self.start_date)
        finish_date = (lambda f: f if f else "")(self.finish_date)
        return f"{self.name} ({start_date} >> {finish_date})"
