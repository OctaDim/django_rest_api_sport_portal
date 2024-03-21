from rest_framework import serializers, request
from rest_framework.validators import UniqueValidator

from django.utils.translation import gettext_lazy

from django.db.models import Q

from apps.api.messages_api.messages_non_front import EXCEPTION_INFO

from apps.api.messages_api.messages_errors import (
    USER_REQUIRED,
    CLIENT_CREATOR_REQUIRED,
    CLIENT_WITH_USER_ALREADY_EXISTS,
                                    )

from apps.api.group_many_client.models import GroupManyClient
from apps.api.client.models import Client
from apps.api.user.models import User

from apps.api.training_group.serializers import TrainingGroupAllFieldsModelSerializer


from apps.api.user.serializers import UsersAllFieldsNoPermissionsSerializer

from apps.api.client.validators import validate_image_size



class GroupManyClientModelSerializer(serializers.ModelSerializer):
    training_group_id = TrainingGroupAllFieldsModelSerializer

    client_id = serializers.SlugRelatedField(slug_field="id__username",
                                             queryset=Client.objects.all(),
                                                 read_only=False)

    creator = serializers.SlugRelatedField(slug_field="full_name",
                                                 read_only=True)

    class Meta:
        model = GroupManyClient
        # fields = "__all__"
        fields = ["id",
                  "training_group_id",
                  "client_id",
                  "created_at",
                  "updated_at",
                  "creator",
                  ]
