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
                    email,     # Named parameters extracted to check them
                    username,  # other values are falling into **extra_fields
                    nickname,
                    first_name,
                    # last_name,
                    # phone,
                    password,
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

        if ERROR_MESSAGES:
            raise ValueError(", ".join(ERROR_MESSAGES))  # todo: Why ValueError interrupting execution (ValidationError)

        user = self.model(
                          # email=email,  # Refactored. Extracted named params, unusefull because values in extra_fields
                          # username=username,
                          # nickname=nickname,
                          # first_name=first_name,
                          # last_name=last_name,
                          # phone=phone,
                          # password=password,
                          **extra_fields  # All kwarg fields (except password 2) from the serializer validated_data
                          )

        user.set_password(password)
        user.save(using=self._db)

        return user



    def create_superuser(self,
    # IMPORTANT: NOT TO RENAME FOR DJANGO CREATE SUPERUSER CONSOLE COMMAND WORKING GOOD
                         email,     # Named parameters extracted to check them
                         username,  # others values are falling into **extra_fields
                         nickname,
                         first_name,
                         # last_name,
                         # phone,
                         password,
                         **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # extra_fields.setdefault("is_verified", True)


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

        if not first_name:
            ERROR_MESSAGES.append(gettext_lazy(FIRST_NAME_REQUIRED_MESSAGE))
            # raise ValueError(gettext_lazy(FIRST_NAME_REQUIRED_MESSAGE))

        if ERROR_MESSAGES:
            raise ValueError(ERROR_MESSAGES)

        user = self.model(
                          # email=email,  # Refactored. Extracted named params, unusefull because values in extra_fields
                          # username=username,
                          # nickname=nickname,
                          # first_name=first_name,
                          # last_name=last_name,
                          # phone=phone,
                          # password=password,
                          **extra_fields,  # All kwarg fields (except password 2) from the serializer validated_data
                          )

        user.set_password(password)
        user.save(using=self._db)

        return user



    # def create_custom_staff_superuser(self,  # todo: Make create_custom_staff_superuser method
    #                      email,  # Named parameters extracted to check them
    #                      username,  # others values are falling into **extra_fields
    #                      nickname,
    #                      first_name,
    #                      # last_name,
    #                      # phone,
    #                      password,
    #                      # is_staff,        # Will be set True by default for superuser, see below
    #                      # is_superuser,    # Will be set True by default for superuser, see below
    #                      # is_verified,     # Will be set True by default for superuser, see below
    #                      **extra_fields):
    #
    #     extra_fields.setdefault("is_staff", True)
    #     extra_fields.setdefault("is_superuser", True)
    #
    #     ERROR_MESSAGES = []
    #     # if not extra_fields.get("is_staff"):  # uncomment, if not set by default for the superuser above
    #     #     ERROR_MESSAGES.append(gettext_lazy(NOT_IS_STAFF_ERROR))
    #     #     # raise ValueError(gettext_lazy(NOT_IS_STAFF_ERROR))
    #     #
    #     # if not extra_fields.get("is_superuser"):  # uncomment, if not set by default for the superuser above
    #     #     ERROR_MESSAGES.append(gettext_lazy(NOT_IS_SUPERUSER_ERROR))
    #     #     # raise ValueError(gettext_lazy(NOT_IS_SUPERUSER_ERROR))
    #     #
    #     # if not extra_fields.get("is_verified"):  # uncomment, if not set by default for the superuser above
    #     #     ERROR_MESSAGES.append(gettext_lazy(NOT_IS_SUPERUSER_ERROR))
    #     #     # raise ValueError(gettext_lazy(NOT_IS_SUPERUSER_ERROR))
    #
    #     if not email:
    #         ERROR_MESSAGES.append(gettext_lazy(EMAIL_REQUIRED_MESSAGE))
    #         # raise ValueError(gettext_lazy(EMAIL_REQUIRED_MESSAGE))
    #     else:
    #         email = self.normalize_email(email=email)
    #         # self.email_validator(email=email)  # Temporally switched off
    #
    #     if not username:
    #         ERROR_MESSAGES.append(gettext_lazy(USERNAME_REQUIRED_MESSAGE))
    #         # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))
    #
    #     if not nickname:
    #         ERROR_MESSAGES.append(gettext_lazy(NICKNAME_REQUIRED_MESSAGE))
    #         # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))
    #
    #     if not first_name:
    #         ERROR_MESSAGES.append(gettext_lazy(FIRST_NAME_REQUIRED_MESSAGE))
    #         # raise ValueError(gettext_lazy(FIRST_NAME_REQUIRED_MESSAGE))
    #
    #     if ERROR_MESSAGES:
    #         raise ValueError(ERROR_MESSAGES)
    #
    #     user = self.model(
    #         # email=email,  # Refactored. Extracted named params, unusefull because values in extra_fields
    #         # username=username,
    #         # nickname=nickname,
    #         # first_name=first_name,
    #         # last_name=last_name,
    #         # phone=phone,
    #         # password=password,
    #         **extra_fields,  # All kwarg fields (except password 2) from the serializer validated_data
    #     )
    #
    #     user.set_password(password)
    #     user.save(using=self._db)
    #
    #     return user
