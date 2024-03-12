from django.db import models

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_fields import (GROUP_CLIENT,
                                                   GROUPS_CLIENTS,
                                                   TRAINING_GROUP,
                                                   CLIENT,
                                                   CREATED_AT,
                                                   UPDATED_AT,
                                                   CREATOR,
                                                   )

from apps.api.user.models import User
from apps.api.client.models import Client
# from apps.api.training_group.models import TrainingGroup  # Replaced by "training_group.TrainingGroup" direct link



class GroupManyClient(models.Model):
    training_group_id = models.ForeignKey(
                                to="training_group.TrainingGroup",  # Direct text reference to fix import cycling error
                                on_delete=models.PROTECT,
                                related_name="group_many_client",
                                verbose_name=gettext_lazy(TRAINING_GROUP),
                                )

    client_id = models.ForeignKey(Client,
                                  on_delete=models.PROTECT,
                                  related_name="group_many_client",
                                  verbose_name=gettext_lazy(CLIENT),
                                  )

    created_at = models.DateTimeField(auto_now_add=True,
                                        verbose_name=gettext_lazy(CREATED_AT))

    updated_at = models.DateTimeField(auto_now=True,
                                        verbose_name=gettext_lazy(UPDATED_AT))

    creator = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                related_name="group_many_client",
                                verbose_name=gettext_lazy(CREATOR))

    class Meta:
        verbose_name = gettext_lazy(GROUP_CLIENT)
        verbose_name_plural = gettext_lazy(GROUPS_CLIENTS)
        ordering = ["training_group_id", "client_id"]
        unique_together = ["training_group_id", "client_id"]

    def __str__(self):
        return (
                # f"{self.training_group_id.department} > "
                f"{self.training_group_id.training_group_code} > "
                f"{self.training_group_id.training_group_name} > "
                f"{self.client_id.user}"
                )
