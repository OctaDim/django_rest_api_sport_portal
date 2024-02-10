from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy

# ##################################################################
# from django.contrib.auth.models import User  # Django default user
from apps.api.user.models import User  # Custom user
# ##################################################################

from apps.api.messages import (ENTER_EMAIL_LIKE_MSG,
                               ENTER_USERNAME_MSG,
                               ENTER_NICKNAME_MSG,
                               ENTER_PASSWORD_MSG,
                               REPEAT_PASSWORD_MSG,
                               ENTER_FIRSTNAME_MSG,
                               )

from apps.api.messages_errors import (PASSWORD_REQUIRED_MSG,
                                      PASSWORD2_REQUIRED_MSG,
                                      PASSWORDS_NOT_MATCH_ERROR,
                                      EMAIL_ALREADY_EXISTS,
                                      USERNAME_ALREADY_EXISTS,
                                      NICKNAME_ALREADY_EXISTS,
                                      )


class UserRegistrySerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
        # validators=[UniqueValidator(queryset=User.objects.all())],
        style={"placeholder": gettext_lazy(ENTER_EMAIL_LIKE_MSG)}, )

    username = serializers.CharField(
        max_length=30,
        # validators=[UniqueValidator(queryset=User.objects.all())],
        style={"placeholder": gettext_lazy(ENTER_USERNAME_MSG)}, )

    nickname = serializers.CharField(
        max_length=50,
        # validators=[UniqueValidator(queryset=User.objects.all())],
        style={"placeholder": gettext_lazy(ENTER_NICKNAME_MSG)}, )

    first_name = serializers.CharField(
        max_length=30,
        validators=[UniqueValidator(queryset=User.objects.all())],
        style={"placeholder": gettext_lazy(ENTER_FIRSTNAME_MSG)}, )

    last_name = serializers.CharField(
        max_length=30,
        required=False, )

    phone = serializers.CharField(
        max_length=100,
        required=False, )

    password = serializers.CharField(
        min_length=4, max_length=30,
        write_only=True,
        style={"input_type": "password",
               "placeholder": gettext_lazy(ENTER_PASSWORD_MSG)}, )

    password2 = serializers.CharField(
        min_length=4, max_length=30,
        write_only=True,
        style={"input_type": "password",
               "placeholder": gettext_lazy(REPEAT_PASSWORD_MSG)}, )

    class Meta:
        model = User
        fields = ["email",
                  "username",
                  "nickname",
                  "first_name",
                  "last_name",
                  "phone",
                  "password",
                  "password2",
                  ]

    def _validate_email_uniqueness(self, email_to_check:str, **attrs): # todo: transfer validation from validate method
        pass

    def _validate_username_uniqueness(self, username_to_check:str, **attrs):  # todo: transfer validation from validate method
        pass

    def _validate_nickname_uniqueness(self, nickname_to_check:str, **attrs):  # todo: transfer validation from validate method
        pass


    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        ERROR_MESSAGES = []

        if not password:
            ERROR_MESSAGES.append(gettext_lazy(PASSWORD_REQUIRED_MSG))
            # raise serializers.ValidationError(
            #     gettext_lazy(PASSWORD_REQUIRED_MSG))

        if not password2:
            ERROR_MESSAGES.append(gettext_lazy(PASSWORD2_REQUIRED_MSG))
            # raise serializers.ValidationError(
            #     gettext_lazy(PASSWORD2_REQUIRED_MSG))

        if password != password2:
            ERROR_MESSAGES.append(gettext_lazy(PASSWORDS_NOT_MATCH_ERROR))
            # raise serializers.ValidationError(
            #     gettext_lazy(PASSWORDS_NOT_MATCH_ERROR))


        # ##############################################################
        # ## OPTIONAL, IF NOT DEFINED UNIQUENESS IN SERIAL PARAMETERS ##
        # ##############################################################
        email_to_check = attrs.get("email")
        if User.objects.filter(email=email_to_check).exists():
            ERROR_MESSAGES.append(gettext_lazy(EMAIL_ALREADY_EXISTS))
            # raise serializers.ValidationError(
            #     gettext_lazy(EMAIL_ALREADY_EXISTS))

        username_to_check = attrs.get("username")
        if User.objects.filter(username=username_to_check).exists():
            ERROR_MESSAGES.append(gettext_lazy(USERNAME_ALREADY_EXISTS))
            # raise serializers.ValidationError(
            #     gettext_lazy(USERNAME_ALREADY_EXISTS))

        nickname_to_check=attrs.get("nickname")
        if User.objects.filter(nickname=nickname_to_check).exists():
            ERROR_MESSAGES.append(gettext_lazy(NICKNAME_ALREADY_EXISTS))
            # raise serializers.ValidationError(
            #     gettext_lazy(NICKNAME_ALREADY_EXISTS))
        # ##############################################################
        # ##############################################################


        if ERROR_MESSAGES:
            raise serializers.ValidationError(gettext_lazy(ERROR_MESSAGES))

    def create(self, validated_data):
        user = User.objects.create_user(
                            email=validated_data.get("email"),
                            username=validated_data.get("username"),
                            nickname=validated_data.get("nickname"),
                            first_name=validated_data.get("first_name"),
                            last_name=validated_data.get("last_name"),
                            phone=validated_data.get("phone"),
                            password=validated_data.get("password"),
                            )
        return user
