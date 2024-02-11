from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.backends import UserModel
from django.utils.translation import gettext_lazy

from apps.api.messages_errors import (EMAIL_OR_USERNAME_OR_NICKNAME_REQUIRED_MSG,
                                      PASSWORD_REQUIRED_MSG,
                                      )

from apps.api.messages_errors import USER_NOT_FOUND_MESSAGE


class CustomAuthByEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # print(f"\n##### CUSTOM AUTH BY EMAIL ## AS METHOD ARGUMENTS: "
        #       f"email entered instead of username: {username}")
        # print(f"##### CUSTOM AUTH BY EMAIL ## FROM REQUEST (KWARGS): "
        #       f"email entered instead of username: {kwargs.get("username")}\n")

        if not username:
            username = kwargs.get("username")  # Get username value with entered email on purpose or by mistake

        if not username:
            # gettext_lazy(EMAIL_OR_USERNAME_OR_NICKNAME_REQUIRED_MSG)
            return None

        if not password:
            # gettext_lazy(PASSWORD_REQUIRED_MSG)
            return None

        try:
            user = UserModel.objects.get(email=username)  # Get user by email entered as username
        except UserModel.DoesNotExist:
            # gettext_lazy(USER_NOT_FOUND_MESSAGE(username))

            UserModel().set_password(password)
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                print(f"\n##### CUSTOM AUTH BY EMAIL ## RESULT: User [ {username} ] is authenticated\n")
                return user



class CustomAuthByNickNameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # print(f"\n##### CUSTOM AUTH BY NICKNAME ## AS METHOD ARGUMENTS: "
        #       f"nickname entered instead of username: {username}")
        # print(f"##### CUSTOM AUTH BY NICKNAME ## FROM REQUEST (KWARGS): "
        #       f"nickname entered instead of username: {kwargs.get("username")}\n")

        if not username:
            username = kwargs.get("username")  # Get username value with entered email on purpose or by mistake

        if not username:
            # gettext_lazy(EMAIL_OR_USERNAME_OR_NICKNAME_REQUIRED_MSG)
            return None

        if not password:
            # gettext_lazy(PASSWORD_REQUIRED_MSG)
            return None

        try:
            user = UserModel.objects.get(nickname=username)  # Get user by email entered as username
        except UserModel.DoesNotExist:
            # gettext_lazy(USER_NOT_FOUND_MESSAGE(username))

            UserModel().set_password(password)
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                print(f"\n##### CUSTOM AUTH BY NICKNAME ## RESULT: User [ {username} ] is authenticated\n")
                return user
