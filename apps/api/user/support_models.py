from django.contrib.auth.models import models
from annoying.fields import AutoOneToOneField

from apps.api.user.models import User

class Creator(models.Model):
    id = AutoOneToOneField(User,
                           primary_key=True,
                           on_delete=models.PROTECT,
                           to_field="id",
                           related_name="user_id",
                           )

    # email = AutoOneToOneField(User,
    #                           primary_key=False,
    #                           on_delete=models.PROTECT,
    #                           to_field="email",
    #                           related_name="user_email",
    #                           )

    # username = AutoOneToOneField()
    # nickname = AutoOneToOneField()
    #
    #
    # def __str__(self):
    #     return f"User: {self.username} [ nickname: {self.nickname}, email: {self.email} ]"
