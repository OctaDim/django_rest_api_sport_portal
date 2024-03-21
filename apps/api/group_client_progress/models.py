from django.db import models
# Create your models here.

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_fields import (GROUP_CLIENT_PROGRESS,
                                                   GROUPS_CLIENTS_PROGRESSES,
                                                   GROUP_CLIENT,                                                   SATISFACTION_LEVEL,
                                                   EMOTIONAL_LEVEL,
                                                   CHECK_POINT_DATE,
                                                   TASK_COMPLETED,
                                                   CURRENT_WEIGHT,
                                                   CURRENT_BREAST,
                                                   CURRENT_SHOULDERS,
                                                   CURRENT_WAIST,
                                                   CURRENT_HIPS,
                                                   CURRENT_HEIGHT,
                                                   DESCRIPTION,
                                                   NOTE,
                                                   CREATED_AT,
                                                   UPDATED_AT,
                                                   CREATOR,
                                                   )

from apps.api.user.models import User
from apps.api.group_many_client.models import GroupManyClient
from apps.api.self_satisfaction_level.models import SelfSatisfactionLevel
from apps.api.emotional_level.models import EmotionalLevel
from apps.api.client.models import Client
from apps.api.coach.models import Coach

from apps.api.utils.utils import number_or_str_to_abs_float



class GroupClientProgress(models.Model):
    group_many_client = models.ForeignKey(
                                GroupManyClient,
                                on_delete=models.PROTECT,
                                related_name="group_client_progress",
                                verbose_name=gettext_lazy(GROUP_CLIENT))

    self_satisfaction_level = models.ForeignKey(
                                SelfSatisfactionLevel,
                                on_delete=models.PROTECT,
                                related_name="group_client_progress",
                                verbose_name=gettext_lazy(SATISFACTION_LEVEL))

    emotional_level = models.ForeignKey(
                                EmotionalLevel,
                                on_delete=models.PROTECT,
                                related_name="group_client_progress",
                                verbose_name=gettext_lazy(EMOTIONAL_LEVEL))

    task_completed = models.BooleanField(
                                default=False,
                                verbose_name=gettext_lazy(TASK_COMPLETED))

    check_point_date = models.DateField(
                                verbose_name=gettext_lazy(CHECK_POINT_DATE))

    current_weight = models.FloatField(
                                blank=True, null=True,
                                validators=[number_or_str_to_abs_float],
                                verbose_name=gettext_lazy(CURRENT_WEIGHT))

    current_breast = models.FloatField(
                                blank=True, null=True,
                                validators=[number_or_str_to_abs_float],
                                verbose_name=gettext_lazy(CURRENT_BREAST))

    current_shoulders = models.FloatField(
                                blank=True, null=True,
                                validators=[number_or_str_to_abs_float],
                                verbose_name=gettext_lazy(CURRENT_SHOULDERS))

    current_waist = models.FloatField(
                                blank=True, null=True,
                                validators=[number_or_str_to_abs_float],
                                verbose_name=gettext_lazy(CURRENT_WAIST))

    current_hips = models.FloatField(
                                blank=True, null=True,
                                validators=[number_or_str_to_abs_float],
                                verbose_name=gettext_lazy(CURRENT_HIPS))

    current_height = models.FloatField(
                                blank=True, null=True,
                                validators=[number_or_str_to_abs_float],
                                verbose_name=gettext_lazy(CURRENT_HEIGHT))

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
                                related_name='group_client_progress',
                                verbose_name=gettext_lazy(CREATOR))

    class Meta:
        unique_together = ["check_point_date","group_many_client"]
        verbose_name = gettext_lazy(GROUP_CLIENT_PROGRESS)
        verbose_name_plural = gettext_lazy(GROUPS_CLIENTS_PROGRESSES)
        ordering = ["check_point_date",
                    # "group_many_client",
                    ]

    def __str__(self):
        return f"{self.check_point_date}: {self.group_many_client}"
