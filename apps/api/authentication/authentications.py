from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.backends import UserModel


class CustomAuthByEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username:
            username = kwargs.get("username")  # Get username value with entered email on purpose or by mistake

        if not username:
            return None

        if not password:
            return None

        try:
            user = UserModel.objects.get(email=username)  # Get user by email entered as username
        except UserModel.DoesNotExist:

            UserModel().set_password(password)
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                print(f"\n##### CUSTOM AUTH BY EMAIL ## RESULT: User [ {username} ] is authenticated\n")
                return user



class CustomAuthByNickNameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username:
            username = kwargs.get("username")  # Get username value with entered email on purpose or by mistake

        if not username:
            return None

        if not password:
            return None

        try:
            user = UserModel.objects.get(nickname=username)  # Get user by email entered as username
        except UserModel.DoesNotExist:

            UserModel().set_password(password)
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                print(f"\n##### CUSTOM AUTH BY NICKNAME ## RESULT: User [ {username} ] is authenticated\n")
                return user
