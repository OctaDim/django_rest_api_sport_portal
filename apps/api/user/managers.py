from django.contrib.auth.models import BaseUserManager  # For the custom user model

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy

from apps.api.messages_errors import (INVALID_EMAIL_ERROR,
                                      EMAIL_REQUIRED_MESSAGE,
                                      USERNAME_REQUIRED_MESSAGE,
                                      NICKNAME_REQUIRED_MESSAGE,
                                      FIRST_NAME_REQUIRED_MESSAGE,
                                      LAST_NAME_REQUIRED_MESSAGE,
                                      PHONE_REQUIRED_MESSAGE,
                                      NOT_IS_STAFF_ERROR,
                                      NOT_IS_SUPERUSER_ERROR,
                                      )



class UserManager(BaseUserManager):

    def email_validator(self, email):
        try:
            validate_email(email)

        except ValidationError as error:
            raise ValueError(
                gettext_lazy(INVALID_EMAIL_ERROR(error.message)))


    def create_user(self,
                    email=None,     # Named parameters extracted to check or make ops
                    username=None,  # others falling into **extra_fields
                    nickname=None,
                    first_name=None,
                    last_name=None,
                    phone=None,
                    password=None,
                    **extra_fields):

        ERROR_MESSAGES = []
        if not email:
            ERROR_MESSAGES.append(gettext_lazy(EMAIL_REQUIRED_MESSAGE))
            # raise ValueError(gettext_lazy(EMAIL_REQUIRED_MESSAGE))
        else:
            email = self.normalize_email(email=email)
            # self.email_validator(email=email)  # Temporally switched off

        if not username:
            ERROR_MESSAGES.append(gettext_lazy(USERNAME_REQUIRED_MESSAGE))
            # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))

        if not nickname:
            ERROR_MESSAGES.append(gettext_lazy(NICKNAME_REQUIRED_MESSAGE))
            # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))

        if not first_name:
            ERROR_MESSAGES.append(gettext_lazy(FIRST_NAME_REQUIRED_MESSAGE))
            # raise ValueError(gettext_lazy(FIRST_NAME_REQUIRED_MESSAGE))

        # if not last_name:  # Uncomment, if necessary
        #     ERROR_MESSAGES.append(gettext_lazy(LAST_NAME_REQUIRED_MESSAGE))
        #     # raise ValueError(gettext_lazy(LAST_NAME_REQUIRED_MESSAGE))

        # if not phone:  # Uncomment, if necessary
        #     ERROR_MESSAGES.append(gettext_lazy(PHONE_REQUIRED_MESSAGE))
        #     # raise ValueError(gettext_lazy(PHONE_REQUIRED_MESSAGE))

        if ERROR_MESSAGES:
            raise ValueError(", ".join(ERROR_MESSAGES))

        user = self.model(email=email,  # Named parameters extracted to check or make ops
                          username=username,
                          nickname=nickname,
                          first_name=first_name,
                          last_name=last_name,
                          phone=phone,
                          password=password,
                          **extra_fields  # Other kwarg fields, that are in not named parameters
                          )

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self,  # NOT TO RENAME FOR DJANGO CREATE SUPERUSER CONSOLE COMMAND WORKING GOOD
                         email=None,  # Named parameters extracted to check or make ops
                         username=None,  # others falling into **extra_fields
                         nickname=None,
                         first_name=None,
                         last_name=None,
                         phone=None,
                         password=None,
                         # is_staff=None,  # Commented, because if None, set True by default for superuser, see below
                         # is_superuser=None,  # Commented, because if None, set True by default for superuser, see below
                         # is_verified=None,  # Commented, because if None, set True by default for superuser, see below
                         **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        ERROR_MESSAGES = []
        # if not extra_fields.get("is_staff"):  # uncomment, if not set by default for the superuser above
        #     ERROR_MESSAGES.append(gettext_lazy(NOT_IS_STAFF_ERROR))
        #     # raise ValueError(gettext_lazy(NOT_IS_STAFF_ERROR))
        #
        # if not extra_fields.get("is_superuser"):  # uncomment, if not set by default for the superuser above
        #     ERROR_MESSAGES.append(gettext_lazy(NOT_IS_SUPERUSER_ERROR))
        #     # raise ValueError(gettext_lazy(NOT_IS_SUPERUSER_ERROR))
        #
        # if not extra_fields.get("is_verified"):  # uncomment, if not set by default for the superuser above
        #     ERROR_MESSAGES.append(gettext_lazy(NOT_IS_SUPERUSER_ERROR))
        #     # raise ValueError(gettext_lazy(NOT_IS_SUPERUSER_ERROR))

        if not email:
            ERROR_MESSAGES.append(gettext_lazy(EMAIL_REQUIRED_MESSAGE))
            # raise ValueError(gettext_lazy(EMAIL_REQUIRED_MESSAGE))
        else:
            email = self.normalize_email(email=email)
            # self.email_validator(email=email)  # Temporally switched off

        if not username:
            ERROR_MESSAGES.append(gettext_lazy(USERNAME_REQUIRED_MESSAGE))
            # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))

        if not nickname:
            ERROR_MESSAGES.append(gettext_lazy(NICKNAME_REQUIRED_MESSAGE))
            # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))

        if ERROR_MESSAGES:
            raise ValueError(ERROR_MESSAGES)

        user = self.model(email=email,  # Named parameters extracted to check or make ops
                          username=username,
                          nickname=nickname,
                          first_name=first_name,
                          last_name=last_name,
                          phone=phone,
                          password=password,
                          **extra_fields,    # Other kwarg fields, that are in not named parameters
                          )

        user.set_password(password)
        user.save(using=self._db)

        return user
