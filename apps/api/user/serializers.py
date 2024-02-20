from rest_framework import serializers
from apps.api.user.custom_fields import BOOLEAN_CHOICES

# ##################################################################
# from django.contrib.auth.models import User  # Django default user
from apps.api.user.models import User  # Custom user
# ##################################################################



class UsersSerializerAllFields(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ["password"]


class UsersSerializerLimitFields(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",
                  "email",
                  "username",
                  "nickname",
                  "first_name",
                  "last_name",
                  "phone",
                  "is_staff",
                  "is_trainer",
                  "is_verified",
                  "is_active",
                  "date_joined",
                  "last_login",
                  "updated_at",
                  # "creator"
                  )


class UserInfoByIdAllFieldsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = "__all__"  # Not used, if exclude is used (exclude= all-exclude)
        exclude = ["password",
                   "is_verified",
                   "date_joined",
                   "last_login",
                   "updated_at",
                   # "creator"
                   ]


class UserInfoByIdLimitedFieldsSerializer(serializers.ModelSerializer):
    is_staff = serializers.ReadOnlyField()
    is_trainer = serializers.ReadOnlyField()
    is_superuser = serializers.ReadOnlyField()
    is_verified =  serializers.ReadOnlyField()
    is_active = serializers.BooleanField(allow_null=False, initial=True)  # IMPORTANT: Works properly only if default is not defined
    # is_active = serializers.ChoiceField(choices=BOOLEAN_CHOICES)

    class Meta:
        model = User
        fields = ("id",
                  "email",
                  "username",
                  "nickname",
                  "first_name",
                  "last_name",
                  "phone",
                  "is_staff",
                  "is_trainer",
                  "is_superuser",
                  "is_active",
                  "is_verified",
                  "date_joined",
                  "last_login",
                  "updated_at",
                  # "creator"
                  )


    # ########## BASIC, OFTEN USED SERIALIZERS METHODS #################
    # def to_internal_value(self, data):  # Pre-actions before validation (Call: ser.is_valid)
    #     return ret

    # def validate_<field_name>(self, value):  # Certain field validation (Call: ser.is_valid)
    #     return value

    # def validate(self, attrs):  # Several fields validation (Call: ser.is_valid)
    #     return attrs

    # def create(self, validated_data):  # By default executing <Model>.objects.<create>(..) (Call: ser.save()) Would be correct, if to run manager’s get_or_create() instead of manager’s create()
    #     return instance  # Return Model object

    # def update(self, instance, validated_data):
    #     return instance # Return Model object
    # ##################################################################
