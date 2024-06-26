from django.db import models
from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_fields import (SATISFACTION_LEVEL,
                                                   SATISFACTION_LEVELS,
                                                   SATISFACTION_LEVEL_NAME,
                                                   SATISFACTION_LEVEL_VALUE,
                                                   SATISFACTION_LEVEL_ICON_LINK,
                                                   DESCRIPTION,
                                                   CREATED_AT,
                                                   UPDATED_AT,
                                                   CREATOR,
                                                   )

from apps.api.user.models import User

from django_resized import ResizedImageField

from apps.api.self_satisfaction_level.utils import get_image_file_name

from apps.api.self_satisfaction_level.validators import (
                                    validate_satisfaction_level_value)



class SelfSatisfactionLevel(models.Model):
    icon_link = ResizedImageField(  # Option 1, more simple: instead of PIL (pillow) lib (see bellow)
                    upload_to=get_image_file_name,
                    size=[150,150],
                    quality=100,
                    blank=True, null=True,
                    verbose_name=gettext_lazy(SATISFACTION_LEVEL_ICON_LINK))

    # icon_link = models.ImageField(  # Option 2, more advanced: to resize image via PIL (pillow) lib
    #                 upload_to=get_image_file_name,
    #                 blank=True, null=True,
    #                 verbose_name=gettext_lazy(SATISFACTION_LEVEL_ICON_LINK))

    value = models.SmallIntegerField(
                            unique=True,
                            validators=[validate_satisfaction_level_value],
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
                                related_name="self_satisfaction_level",
                                verbose_name=gettext_lazy(CREATOR))

    class Meta:
        verbose_name = gettext_lazy(SATISFACTION_LEVEL)
        verbose_name_plural = gettext_lazy(SATISFACTION_LEVELS)
        ordering = ["value"]


    def __str__(self):
        return f"{self.value} ({self.name})"


    @property
    def full_name(self):
        return f"{self.value} ({self.name})"



    # def save(self, *args, **kwargs):  # Option 2, more advanced: to resize image via PIL (pillow) lib
    #     super().save(*args, **kwargs)
    #     with Image.open(self.icon_link.path) as img:  # PIL.Image.open()
    #         img = img.resize((150, 150))
    #         img.save(self.icon_link.path, quality=100)
