from rest_framework import serializers

# ##################################################################
# from django.contrib.auth.models import User  # Django default user
from apps.api.user.models import User  # Custom user
# ##################################################################

class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",
                  "email",
                  "username",
                  "nickname",
                  "first_name",
                  "last_name",
                  "phone",
                  "date_joined",
                  "last_login",
                  "is_verified",
                  )


class UserInfoByIdAllFieldsSerializer(serializers.ModelSerializer):
    # updated = serializers.ReadOnlyField()
    # is_verified = serializers.ReadOnlyField()

    class Meta:
        model = User
        # fields = "__all__"  # Not used, if exclude is used (exclude= all-exclude)
        exclude = ["password",
                   "is_verified",
                   "date_joined",
                   "last_login",
                   "updated",
                   ]
