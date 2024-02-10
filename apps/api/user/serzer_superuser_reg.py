from apps.api.user.serzer_user_reg import UserRegistrySerializer
from rest_framework.fields import BooleanField

# ##################################################################
# from django.contrib.auth.models import User  # Django default user
from apps.api.user.models import User  # Custom user
# ##################################################################



class CustomTrueByDefaultBooleanField(BooleanField):
    default_empty_html = True
    initial = True


class SuperUserRegistrySerializer(UserRegistrySerializer):  # Inherited from the ordinal user serializer
    is_staff = CustomTrueByDefaultBooleanField()
    is_superuser = CustomTrueByDefaultBooleanField()
    is_verified = CustomTrueByDefaultBooleanField()

    class Meta:
        model = User
        abstract = True
        fields = ["email",
                  "username",
                  "nickname"
                  "first_name",
                  "last_name",
                  "phone",
                  "password",
                  "password2",
                  "is_staff",
                  "is_superuser",
                  "is_verified"
                  ]

    def create(self, validated_data):
        user = User.objects.create_superuser(
                        email=validated_data.get("email"),
                        username=validated_data.get("username"),
                        nickname=validated_data.get("nickname"),
                        first_name=validated_data.get("first_name"),
                        last_name=validated_data.get("last_name"),
                        phone=validated_data.get("phone"),
                        password=validated_data.get("password"),
                        is_staff=validated_data.get("is_staff"),
                        is_superuser=validated_data.get("is_superuser"),
                        is_verified=validated_data.get("is_verified"),
                        )
        return user
