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
    # email = serializers.EmailField(  # Temporally switched off email validation by defining field type
    email = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())],
        style={"placeholder": gettext_lazy(ENTER_EMAIL_LIKE_MSG)}, )

    username = serializers.CharField(
        max_length=30,
        validators=[UniqueValidator(queryset=User.objects.all())],
        style={"placeholder": gettext_lazy(ENTER_USERNAME_MSG)}, )

    nickname = serializers.CharField(
        max_length=50,
        validators=[UniqueValidator(queryset=User.objects.all())],
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

    is_staff = serializers.BooleanField(read_only=True)  # To see in Response and for my custom trial creating users
    is_superuser = serializers.BooleanField(read_only=True)  # To see in Response and for my custom trial creating users
    is_verified = serializers.BooleanField(read_only=True)  # To see in Response and for my custom trial creating users

    class Meta:
        model = User
        # abstract = True  # If True, model will not create db table, only for inheritance
        fields = ["email",
                  "username",
                  "nickname",
                  "first_name",
                  "last_name",
                  "phone",
                  "password",
                  "password2",
                  "is_staff"
                  "is_superuser"
                  "is_verified"
                  ]


    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        ERROR_MESSAGES = []

        if not password:
            ERROR_MESSAGES.append(PASSWORD_REQUIRED_MSG)
            # raise serializers.ValidationError(
            #     gettext_lazy(PASSWORD_REQUIRED_MSG))

        if not password2:
            ERROR_MESSAGES.append(PASSWORD2_REQUIRED_MSG)
            # raise serializers.ValidationError(
            #     gettext_lazy(PASSWORD2_REQUIRED_MSG))

        if password != password2:
            ERROR_MESSAGES.append(PASSWORDS_NOT_MATCH_ERROR)
            # raise serializers.ValidationError(
            #     gettext_lazy(PASSWORDS_NOT_MATCH_ERROR))


        # ##############################################################
        # ## OPTIONAL, IF NOT DEFINED UNIQUENESS IN SERIAL PARAMETERS ##
        # ## SERIALIZERS PARAMETERS IS CHECKING FIRST, WHEN SERIALIZER
        # ## OBJECT CREATED, VALIDATE METHOD IS EXECUTING LATER IN VIEWS
        # ##############################################################
        # email_to_check = attrs.get("email")
        # if User.objects.filter(email=email_to_check).exists():
        #     ERROR_MESSAGES.append(EMAIL_ALREADY_EXISTS)
        #     # raise serializers.ValidationError(
        #     #     gettext_lazy(EMAIL_ALREADY_EXISTS))
        #
        # username_to_check = attrs.get("username")
        # if User.objects.filter(username=username_to_check).exists():
        #     ERROR_MESSAGES.append(USERNAME_ALREADY_EXISTS)
        #     # raise serializers.ValidationError(
        #     #     gettext_lazy(USERNAME_ALREADY_EXISTS))
        #
        # nickname_to_check=attrs.get("nickname")
        # if User.objects.filter(nickname=nickname_to_check).exists():
        #     ERROR_MESSAGES.append(NICKNAME_ALREADY_EXISTS)
        #     # raise serializers.ValidationError(
        #     #     gettext_lazy(NICKNAME_ALREADY_EXISTS))
        # ##############################################################
        # ##############################################################


        if ERROR_MESSAGES:
            ERROR_MESSAGES_STR = ", ".join(ERROR_MESSAGES)
            raise serializers.ValidationError(gettext_lazy(ERROR_MESSAGES_STR))  # todo: ValidationError writes non-field errors

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")  # Refactored to avoid tedious getting values from validated_data via get()
        print(validated_data)
        user = User.objects.create_user(
                            # email=validated_data.get("email"),  # Refactored. Passing as **validated_data dictionary,
                            # username=validated_data.get("username"),  # instead of huge qty of the named parameters
                            # nickname=validated_data.get("nickname"),
                            # first_name=validated_data.get("first_name"),
                            # last_name=validated_data.get("last_name"),
                            # phone=validated_data.get("phone"),
                            # password=validated_data.get("password"),
                            # is_staff=validated_data.get("is_staff"),
                            # is_superuser=validated_data.get("is_superuser"),
                            # is_verified=validated_data.get("is_verified"),
                            **validated_data
                            )
        return user
