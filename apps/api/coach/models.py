from django.db import models
from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_fields import (USER,
                                                   COACH,
                                                   COACHES,
                                                   COACH_SPECIALITY,
                                                   FIRST_NAME,
                                                   LAST_NAME,
                                                   PHONE,
                                                   COUNTRY,
                                                   ADDRESS,
                                                   GENDER,
                                                   BIRTH_DATE,
                                                   BIBLIOGRAPHY,
                                                   NOTE,
                                                   AVATAR_THUMBNAIL_LINK,
                                                   CREATED_AT,
                                                   UPDATED_AT,
                                                   COACH_CREATOR)

from apps.api.user.models import User
from apps.api.coach_speciality.models import CoachSpeciality
from apps.api.country.models import Country
from apps.api.gender.models import Gender

from apps.api.coach.utils import get_image_file_name
from apps.api.coach.validators import validate_image_size



class Coach(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.PROTECT,
                                related_name="coach",
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

    coach_speciality = models.ForeignKey(
                            CoachSpeciality,
                            on_delete=models.PROTECT,
                            blank=True, null=True,
                            related_name="coach",
                            verbose_name=gettext_lazy(COACH_SPECIALITY))

    first_name = models.CharField(max_length=30,
                                  blank=True, null=True,
                                  verbose_name=gettext_lazy(FIRST_NAME))

    last_name = models.CharField(max_length=30,
                                 blank=True, null=True,
                                 verbose_name=gettext_lazy(LAST_NAME))

    phone = models.CharField(max_length=100,
                             blank=True, null=True,
                             verbose_name=gettext_lazy(PHONE))

    country = models.ForeignKey(Country,
                                on_delete=models.PROTECT,
                                blank=True, null=True,
                                related_name="coach",
                                verbose_name=gettext_lazy(COUNTRY))

    address = models.TextField(max_length=500,
                               blank=True, null=True,
                               verbose_name=gettext_lazy(ADDRESS))

    gender = models.ForeignKey(Gender,
                               on_delete=models.PROTECT,
                               blank=True, null=True,
                               related_name="coach",
                               verbose_name=gettext_lazy(GENDER))

    birth_date = models.DateField(blank=True, null=True,
                                  verbose_name=gettext_lazy(BIRTH_DATE))

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

    coach_creator = models.ForeignKey(
                            User,
                            on_delete=models.PROTECT,
                            related_name="coaches",
                            verbose_name=gettext_lazy(COACH_CREATOR))

    class Meta:
        verbose_name = gettext_lazy(COACH)
        verbose_name_plural = gettext_lazy(COACHES)
        ordering = ["user__email", "user__username", "user__nickname"]

    def __str__(self):
        return f"{self.user.nickname} [{self.user.email}]"


    @property
    def full_name(self):
        return (f"username: {self.user.username}, "
                f"nickname: {self.user.nickname}, "
                f"email: {self.user.email}")


    def save(self, *args, **kwargs):
        # SIGNAL EXECUTING HERE: Before super() pre_save signal executes (apps.api.administrator.signals)
        super().save(*args, **kwargs)  # Origin method creating and saving new object record
        # SIGNAL EXECUTING HERE: After super() post_save signal executes (apps.api.administrator.signals)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # SIGNAL EXECUTING HERE: After super() post_delete signal executes (apps.api.administrator.signals)
