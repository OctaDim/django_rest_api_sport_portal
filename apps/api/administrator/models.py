from django.db import models
from django.utils.translation import gettext_lazy

from apps.api.messages_fields import (USER,
                                      ADMINISTRATOR,
                                      ADMINISTRATORS,
                                      BIBLIOGRAPHY,
                                      NOTE,
                                      AVATAR_THUMBNAIL_LINK,
                                      CREATED_AT,
                                      UPDATED_AT,
                                      ADMINISTRATOR_CREATOR)

from apps.api.user.models import User

from django_resized import ResizedImageField

from apps.api.administrator.utils import get_image_file_name
from apps.api.administrator.validators import validate_image_size



class Administrator(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.PROTECT,
                                related_name="administrator",
                                verbose_name=gettext_lazy(USER))

    # thumbnail_link = ResizedImageField(     # Option 1, more simple: instead of PIL (pillow) lib (see bellow)
    #     upload_to=get_image_file_name,
    #     size=[150, 150],
    #     quality=100,
    #     blank=True, null=True,
    #     verbose_name=gettext_lazy(AVATAR_THUMBNAIL_LINK))

    thumbnail_link = models.ImageField(  # Option 2, more advanced: to resize image via PIL (pillow) lib
                            upload_to=get_image_file_name,
                            blank=True, null=True,
                            validators=[validate_image_size],
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

    administrator_creator = models.ForeignKey(
                            User,
                            on_delete=models.PROTECT,
                            related_name="administrators",
                            verbose_name=gettext_lazy(ADMINISTRATOR_CREATOR))

    class Meta:
        verbose_name = gettext_lazy(ADMINISTRATOR)
        verbose_name_plural = gettext_lazy(ADMINISTRATORS)
        ordering = ["user__email", "user__username", "user__nickname"]

    def __str__(self):
        return f"{self.user.nickname} [{self.user.email}]"


    def save(self, *args, **kwargs):
        # SIGNAL EXECUTING HERE: Before super() pre_save signal executes (apps.api.administrator.signals)
        super().save(*args, **kwargs)  # Origin method creating and saving new object record
        # SIGNAL EXECUTING HERE: After super() post_save signal executes (apps.api.administrator.signals)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # SIGNAL EXECUTING HERE: After super() post_delete signal executes (apps.api.administrator.signals)
