from django.db import models
# Create your models here.

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_fields import (TRAINING_GROUP,
                                                   TRAINING_GROUPS,
                                                   DEPARTMENT,
                                                   TRAINING_YEAR,
                                                   ADMINISTRATOR,
                                                   TRAINING_GROUP_CODE,
                                                   TRAINING_GROUP_NAME,
                                                   DESCRIPTION,
                                                   NOTE,
                                                   START_DATE,
                                                   FINISH_DATE,
                                                   CREATED_AT,
                                                   UPDATED_AT,
                                                   CREATOR,
                                                   CLIENT,
                                                   COACH,
                                                   )

from apps.api.user.models import User
from apps.api.department.models import Department
from apps.api.training_year.models import TrainingYear
from apps.api.administrator.models import Administrator
from apps.api.client.models import Client
from apps.api.coach.models import Coach



class TrainingGroup(models.Model):
    training_group_code = models.CharField(
                        max_length=50,
                        unique=True,
                        verbose_name=gettext_lazy(TRAINING_GROUP_CODE))

    training_group_name = models.CharField(
                        max_length=150,
                        blank=True, null=True,
                        verbose_name=gettext_lazy(TRAINING_GROUP_NAME))

    description = models.TextField(max_length=300,
                                   blank=True, null=True,
                                   verbose_name=gettext_lazy(DESCRIPTION))

    note = models.CharField(max_length=150,
                            blank=True, null=True,
                            verbose_name=gettext_lazy(NOTE))

    training_year = models.ForeignKey(TrainingYear,
                                      on_delete=models.PROTECT,
                                      related_name="training_group",
                                      verbose_name=gettext_lazy(TRAINING_YEAR))

    start_date = models.DateField(verbose_name=gettext_lazy(START_DATE))

    finish_date = models.DateField(verbose_name=gettext_lazy(FINISH_DATE))

    department = models.ForeignKey(Department,
                                   on_delete=models.PROTECT,
                                   related_name = "training_group",
                                   verbose_name = gettext_lazy(DEPARTMENT))

    administrator = models.ManyToManyField(
                                    Administrator,
                                    blank=True,
                                    related_name="training_group",
                                    verbose_name=gettext_lazy(ADMINISTRATOR))

    client = models.ManyToManyField(Client,
                                    blank=True,
                                    related_name="training_group",
                                    verbose_name=gettext_lazy(CLIENT))

    coach = models.ManyToManyField(Coach,
                                   blank=True,
                                   related_name="training_group",
                                   verbose_name=gettext_lazy(COACH))

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=gettext_lazy(CREATED_AT))

    updated_at = models.DateTimeField(auto_now=True,
                                        verbose_name=gettext_lazy(UPDATED_AT))

    creator = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                related_name='training_group',
                                verbose_name=gettext_lazy(CREATOR))

    class Meta:
        verbose_name = gettext_lazy(TRAINING_GROUP)
        verbose_name_plural = gettext_lazy(TRAINING_GROUPS)
        ordering = ["training_group_code",
                    "training_group_name"]

    def __str__(self):
        return f"{self.training_group_code}: [{self.training_group_name}])"
