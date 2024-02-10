from rest_framework import serializers

# ##################################################################
# from django.contrib.auth.models import User  # Django default user
from apps.api.user.models import User  # Custom user
# ##################################################################

class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
