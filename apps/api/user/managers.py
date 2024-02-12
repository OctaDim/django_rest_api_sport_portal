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
                                      SUPERUSER_NOT_IS_STAFF_ERROR,
                                      SUPERUSER_NOT_IS_SUPERUSER_ERROR,
                                      STAFF_NOT_IS_STAFF_ERROR,
                                      )



class UserManager(BaseUserManager):

    def email_validator(self, email):
        try:
            validate_email(email)

        except ValidationError as error:
            raise ValueError(
                gettext_lazy(INVALID_EMAIL_ERROR(error.message)))


    def create_user(self,
                    email,     # Data incoming as dictionary (validated_data from Serializer method 'create_user')
                    username,  # Necessary parameters fall in named parameters to call on them and to check easy
                    nickname,  # other parameters fall in **extra_fields (kwargs)
                    first_name,
                    # last_name,
                    # phone,
                    # is_staff,
                    # is_superuser,
                    # is_verified,
                    password,
                    **extra_fields):

        ERROR_MESSAGES = []
        if not email:
            ERROR_MESSAGES.append(EMAIL_REQUIRED_MESSAGE)
            # raise ValueError(gettext_lazy(EMAIL_REQUIRED_MESSAGE))
        else:
            email = self.normalize_email(email=email)
            # self.email_validator(email=email)  # Temporally switched off

        if not username:
            ERROR_MESSAGES.append(USERNAME_REQUIRED_MESSAGE)
            # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))

        if not nickname:
            ERROR_MESSAGES.append(NICKNAME_REQUIRED_MESSAGE)
            # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))

        if not first_name:
            ERROR_MESSAGES.append(FIRST_NAME_REQUIRED_MESSAGE)
            # raise ValueError(gettext_lazy(FIRST_NAME_REQUIRED_MESSAGE))

        if ERROR_MESSAGES:
            ERRORS_MESSAGES_STR = ", ".join(ERROR_MESSAGES)
            raise ValueError(gettext_lazy(ERRORS_MESSAGES_STR))  # todo: Why ValueError interrupting execution (but ValidationError not)

        user = self.model(
                          email=email,          # All named parameters should specify explicitly, because they
                          username=username,    # were extracted from **extra_fields getting from the dictionary
                          nickname=nickname,    # (incoming validated_data from the Serializer method 'create_user')
                          first_name=first_name,
                          # last_name=last_name,
                          # phone=phone,
                          password=password,
                          **extra_fields  # Other parameters (except password 2) that didn't fall into the named params
                          )

        user.set_password(password)
        user.save(using=self._db)

        return user



    def create_superuser(self,  # IMPORTANT: NOT TO RENAME FOR DJANGO CREATE SUPERUSER CONSOLE COMMAND WORKING GOOD

                         email,     # All named parameters should specify explicitly, because they
                         username,  # were extracted from **extra_fields getting from the dictionary
                         nickname,  # (incoming validated_data from the Serializer method 'create_user')
                         first_name,
                         # last_name,
                         # phone,
                         password,
                         **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        ERROR_MESSAGES = []


        # ##############################################################
        # ### may comment, if set by default for the superuser above ###
        # ##############################################################
        if not extra_fields.get("is_staff"):
            ERROR_MESSAGES.append(SUPERUSER_NOT_IS_STAFF_ERROR)
            # raise ValueError(gettext_lazy(SUPERUSER_NOT_IS_STAFF_ERROR))

        if not extra_fields.get("is_superuser"):  # uncomment, if not set by default for the superuser above
            ERROR_MESSAGES.append(SUPERUSER_NOT_IS_SUPERUSER_ERROR)
            # raise ValueError(gettext_lazy(SUPERUSER_NOT_IS_SUPERUSER_ERROR))
        # ##############################################################
        # ##############################################################

        if not email:
            ERROR_MESSAGES.append(EMAIL_REQUIRED_MESSAGE)
            # raise ValueError(gettext_lazy(EMAIL_REQUIRED_MESSAGE))
        else:
            email = self.normalize_email(email=email)
            # self.email_validator(email=email)  # Temporally switched off

        if not username:
            ERROR_MESSAGES.append(USERNAME_REQUIRED_MESSAGE)
            # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))

        if not nickname:
            ERROR_MESSAGES.append(NICKNAME_REQUIRED_MESSAGE)
            # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))

        if not first_name:
            ERROR_MESSAGES.append(FIRST_NAME_REQUIRED_MESSAGE)
            # raise ValueError(gettext_lazy(FIRST_NAME_REQUIRED_MESSAGE))

        if ERROR_MESSAGES:
            ERROR_MESSAGES_STR = ", ".join(ERROR_MESSAGES)
            raise ValueError(gettext_lazy(ERROR_MESSAGES_STR))

        user = self.model(
                          email=email,  # Refactored. Extracted named params, unusefull because values in extra_fields
                          username=username,
                          nickname=nickname,
                          first_name=first_name,
                          # last_name=last_name,
                          # phone=phone,
                          password=password,
                          **extra_fields,  # All kwarg fields (except password 2) from the serializer validated_data
                          )

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_staff_user(self,
                         email,     # All named parameters should specify explicitly, because they
                         username,  # were extracted from **extra_fields getting from the dictionary
                         nickname,  # (incoming validated_data from the Serializer method 'create_user')
                         first_name,
                         # last_name,
                         # phone,
                         password,
                         **extra_fields):

        extra_fields.setdefault("is_staff", True)

        ERROR_MESSAGES = []

        # ##############################################################
        # ### may comment, if set by default for the staff user above ##
        # ##############################################################
        if not extra_fields.get("is_staff"):
            ERROR_MESSAGES.append(STAFF_NOT_IS_STAFF_ERROR)
            # raise ValueError(gettext_lazy(STAFF_NOT_IS_STAFF_ERROR))
        # ##############################################################
        # ##############################################################


        if not email:
            ERROR_MESSAGES.append(EMAIL_REQUIRED_MESSAGE)
            # raise ValueError(gettext_lazy(EMAIL_REQUIRED_MESSAGE))
        else:
            email = self.normalize_email(email=email)
            # self.email_validator(email=email)  # Temporally switched off

        if not username:
            ERROR_MESSAGES.append(USERNAME_REQUIRED_MESSAGE)
            # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))

        if not nickname:
            ERROR_MESSAGES.append(NICKNAME_REQUIRED_MESSAGE)
            # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))

        if not first_name:
            ERROR_MESSAGES.append(FIRST_NAME_REQUIRED_MESSAGE)
            # raise ValueError(gettext_lazy(FIRST_NAME_REQUIRED_MESSAGE))

        if ERROR_MESSAGES:
            ERROR_MESSAGES_STR = ", ".join(ERROR_MESSAGES)
            raise ValueError(gettext_lazy(ERROR_MESSAGES_STR))

        user = self.model(
                          email=email,  # Refactored. Extracted named params, unusefull because values in extra_fields
                          username=username,
                          nickname=nickname,
                          first_name=first_name,
                          # last_name=last_name,
                          # phone=phone,
                          password=password,
                          **extra_fields,  # All kwarg fields (except password 2) from the serializer validated_data
                          )

        user.set_password(password)
        user.save(using=self._db)

        return user




    # def create_custom_staff_superuser(self,
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
    #     #     ERROR_MESSAGES.append(SUPERUSER_NOT_IS_STAFF_ERROR)
    #     #     # raise ValueError(gettext_lazy(SUPERUSER_NOT_IS_STAFF_ERROR))
    #     #
    #     # if not extra_fields.get("is_superuser"):  # uncomment, if not set by default for the superuser above
    #     #     ERROR_MESSAGES.append(SUPERUSER_NOT_IS_SUPERUSER_ERROR)
    #     #     # raise ValueError(gettext_lazy(SUPERUSER_NOT_IS_SUPERUSER_ERROR))
    #     #
    #     # if not extra_fields.get("is_verified"):  # uncomment, if not set by default for the superuser above
    #     #     ERROR_MESSAGES.append(SUPERUSER_NOT_IS_SUPERUSER_ERROR)
    #     #     # raise ValueError(gettext_lazy(SUPERUSER_NOT_IS_SUPERUSER_ERROR))
    #
    #     if not email:
    #         ERROR_MESSAGES.append(EMAIL_REQUIRED_MESSAGE)
    #         # raise ValueError(gettext_lazy(EMAIL_REQUIRED_MESSAGE))
    #     else:
    #         email = self.normalize_email(email=email)
    #         # self.email_validator(email=email)  # Temporally switched off
    #
    #     if not username:
    #         ERROR_MESSAGES.append(USERNAME_REQUIRED_MESSAGE)
    #         # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))
    #
    #     if not nickname:
    #         ERROR_MESSAGES.append(NICKNAME_REQUIRED_MESSAGE)
    #         # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))
    #
    #     if not first_name:
    #         ERROR_MESSAGES.append(FIRST_NAME_REQUIRED_MESSAGE)
    #         # raise ValueError(gettext_lazy(FIRST_NAME_REQUIRED_MESSAGE))
    #
        # if ERROR_MESSAGES:
        #     ERROR_MESSAGES_STR = ", ".join(ERROR_MESSAGES)
        #     raise ValueError(gettext_lazy(ERROR_MESSAGES_STR))
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
