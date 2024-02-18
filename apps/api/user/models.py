from django.db import models

# Create your models here.
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        AbstractUser)

# ##################################################################
# from django.contrib.auth.models import UserManager  # Django default UserManager
from apps.api.user.managers import UserManager  # Custom user manager
# ##################################################################

from django.utils.translation import gettext_lazy

from apps.api.messages_fields import (EMAIL, USERNAME, NICKNAME,
                                      FIRST_NAME, LAST_NAME, PHONE,
                                      )


class User(AbstractBaseUser, PermissionsMixin):  # todo: Try later to rename CustomUser
    email = models.EmailField(max_length=100,
                              unique=True,
                              verbose_name=gettext_lazy(EMAIL),
                              )

    username = models.CharField(max_length=30,
                                unique=True,
                                verbose_name=gettext_lazy(USERNAME),
                                )

    nickname = models.CharField(max_length=50,
                                unique=True,
                                verbose_name=gettext_lazy(NICKNAME),
                                )

    first_name = models.CharField(max_length=30,
                                  verbose_name=gettext_lazy(FIRST_NAME),
                                  )

    last_name = models.CharField(max_length=30,
                                 blank=True, null=True,
                                 verbose_name=gettext_lazy(LAST_NAME),
                                 )

    phone = models.CharField(max_length=100,
                             blank=True, null=True,
                             verbose_name=gettext_lazy(PHONE))

    is_staff = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email",
                       "nickname",
                       "first_name",
                       # "last_name",
                       # "phone"
                       ]

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["email", "username", "nickname"]


    def __str__(self):
        return f"User: {self.username} [ nickname: {self.nickname}, email: {self.email} ]"


    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
