from django.db import models
from django.utils.translation import gettext_lazy

from apps.api.messages_fields import (ADMINISTRATOR,
                                      ADMINISTRATORS,
                                      BIBLIOGRAPHY,
                                      NOTE,
                                      AVATAR_THUMBNAIL_LINK,
                                      CREATED_AT,
                                      UPDATED_AT,
                                      CREATOR)

from apps.api.messages_errors import ERROR

from apps.api.user.models import User
from apps.api.user.models_secondary import Creator

from django_resized import ResizedImageField
from apps.api.administrator.utils import get_image_file_name



class Administrator(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.PROTECT,
                                related_name="administrator")

    # thumbnail_link = ResizedImageField(     # Option 1, more simple: instead of PIL (pillow) lib (see bellow)
    #     upload_to=get_image_file_name,
    #     size=[150, 150],
    #     quality=100,
    #     blank=True, null=True,
    #     verbose_name=gettext_lazy(AVATAR_THUMBNAIL_LINK))

    thumbnail_link = models.ImageField(  # Option 2, more advanced: to resize image via PIL (pillow) lib
                            upload_to=get_image_file_name,
                            blank=True, null=True,
                            verbose_name=gettext_lazy(AVATAR_THUMBNAIL_LINK))

    bibliography = models.TextField(max_length=500,
                                    blank=True, null=True,
                                    verbose_name=gettext_lazy(BIBLIOGRAPHY))

    note = models.CharField(max_length=150,
                            blank=True, null=True,
                            verbose_name=gettext_lazy(NOTE))

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=gettext_lazy(CREATED_AT))

    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=gettext_lazy(UPDATED_AT))

    creator = models.ForeignKey(Creator,
                                on_delete=models.PROTECT,
                                related_name="administrator",
                                verbose_name=gettext_lazy(CREATOR))

    class Meta:
        verbose_name = gettext_lazy(ADMINISTRATOR)
        verbose_name_plural = gettext_lazy(ADMINISTRATORS)
        ordering = ["user__email", "user__username", "user__nickname"]

    def __str__(self):
        return f"{self.user.nickname} [{self.user.email}]"


    def save(self, *args, **kwargs):
        # IMPORTANT: Before super() executes pre_save signal (apps.api.administrator.signals)
        super().save(*args, **kwargs)  # Origin method creating and saving new object record
        # IMPORTANT: After super() executes post_save signal (apps.api.administrator.signals)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # IMPORTANT: After super() executes post_delete signal (apps.api.administrator.signals)
