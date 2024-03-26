from rest_framework import serializers, request

from rest_framework.validators import UniqueValidator

from django.utils.translation import gettext_lazy

from django.db.models import Q

from apps.api.messages_api.messages_non_front import EXCEPTION_INFO

from apps.api.messages_api.messages_actions import ENTER_INTEGER_NUMBER

from apps.api.messages_api.messages_errors import (
    EMOTIONAL_LEVEL_NAME_REQUIRED,
    EMOTIONAL_LEVEL_VALUE_REQUIRED,
    CREATOR_REQUIRED,
    EMOTIONAL_LEVEL_VALUE_EXISTS,
    EMOTIONAL_LEVEL_NAME_EXISTS,
    NOT_INTEGER_NUMBER,
    LEVEL_VALUE_MIN_LIMIT,
    LEVEL_VALUE_MAX_LIMIT,
    CLIENT_STATUS_REQUIRED, CLIENT_STATUS_EXISTS
)

from apps.api.client_status.models import ClientStatus
from apps.api.user.models import User

from apps.api.utils.utils import (get_integer_from_str_or_number,
                                  number_or_str_to_int)

from apps.api.emotional_level.settings import (EMOTIONAL_LEVEL_VALUE_MIN_LIMIT,
                                               EMOTIONAL_LEVEL_VALUE_MAX_LIMIT)



class ClientStatusAllFieldsModelSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="full_name",
                                           read_only=True)

    class Meta:
        model = ClientStatus
        # fields = "__all__"
        fields = ["id",
                  "name",
                  "description",
                  "created_at",
                  "updated_at",
                  "creator",
                  ]

class ClientStatusCreateModelSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="id",
                                           read_only=False,
                                           queryset=User.objects.all())

    class Meta:
        model = ClientStatus
        # fields = "__all__"
        fields = ["id",
                  "name",
                  "description",
                  "created_at",
                  "updated_at",
                  "creator",
                  ]

    def get_fields(self):
        fields = super().get_fields()

        try:
            current_user_id = self.context["request"].user.id
            fields["creator"].queryset = User.objects.filter(id=current_user_id)
            return fields
        except (ValueError, Exception) as error:
            print(gettext_lazy(EXCEPTION_INFO(error)))
        return fields


    def to_representation(self, instance):  # Forms dictionary with response fields (fields-keys can be added)
        representation = super().to_representation(instance)
        representation["creator"] = str(instance.creator)
        representation["creator_id"] = instance.creator.id
        return representation


    def validate(self, attrs):
        attrs = super().validate(attrs)

        error_messages = []

        name_in_attr = attrs.get("name")
        creator_in_attr = attrs.get("creator")

        if not name_in_attr:
            error_messages.append(CLIENT_STATUS_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CLIENT_STATUS_REQUIRED))

        if not creator_in_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))

        if ClientStatus.objects.filter(name=name_in_attr).exists():
            error_messages.append(CLIENT_STATUS_EXISTS)
            # raise serializers.ValidationError(
            #     gettext_lazy(CLIENT_STATUS_EXISTS))

        if error_messages:
            error_messages_str = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(error_messages_str))

        return attrs



class ClientStatusRetrieveUpdateDeleteModelSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="id",
                                           read_only=False,
                                           queryset=User.objects.all())

    class Meta:
        model = ClientStatus
        # fields = "__all__"
        fields = ["id",
                  "name",
                  "description",
                  "created_at",
                  "updated_at",
                  "creator",
                  ]

    def get_fields(self):
        fields = super().get_fields()

        try:
            current_user_id = self.context["request"].user.id
            fields["creator"].queryset = User.objects.filter(id=current_user_id)
            return fields
        except (ValueError, Exception) as error:
            print(gettext_lazy(EXCEPTION_INFO(error)))
        return fields


    def to_representation(self, instance):  # Forms dictionary with response fields (fields-keys can be added)
        representation = super().to_representation(instance)
        representation["creator"] = str(instance.creator)
        representation["creator_id"] = instance.creator.id
        return representation


    def validate(self, attrs):
        attrs = super().validate(attrs)

        error_messages = []

        name_in_attr = attrs.get("name")
        creator_in_attr = attrs.get("creator")

        if not name_in_attr:
            error_messages.append(CLIENT_STATUS_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CLIENT_STATUS_REQUIRED))

        if not creator_in_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))


        client_status_id_view_passed_req_param = (
            self.context.get("client_status_id"))

        old_client_status_name = ClientStatus.objects.get(
            id=client_status_id_view_passed_req_param).name

        new_client_status_name = attrs.get("name")

        if new_client_status_name != old_client_status_name:
            if ClientStatus.objects.filter(
                    name=new_client_status_name).exists():
                error_messages.append(CLIENT_STATUS_EXISTS)
                # raise serializers.ValidationError(
                #     gettext_lazy(CLIENT_STATUS_EXISTS))


        if error_messages:
            error_messages_str = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(error_messages_str))

        return attrs
