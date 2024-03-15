from rest_framework import serializers, request
from rest_framework.validators import UniqueValidator

from django.utils.translation import gettext_lazy

from django.db.models import Q

from apps.api.messages_api.messages_non_front import EXCEPTION_INFO

from apps.api.messages_api.messages_errors import (
                                    USER_REQUIRED,
                                    CLIENT_CREATOR_REQUIRED,
                                    CLIENT_WITH_THIS_USER_ALREADY_EXISTS_MSG,
                                    )

from apps.api.client.models import Client
from apps.api.user.models import User

from apps.api.user.serializers import UsersAllFieldsNoPermissionsSerializer

from apps.api.client.validators import validate_image_size



class ClientAllFieldsModelSerializer(serializers.ModelSerializer):
    user = UsersAllFieldsNoPermissionsSerializer()

    client_creator = serializers.SlugRelatedField(slug_field="full_name",
                                                  read_only=True)

    class Meta:
        model = Client
        fields = "__all__"



class ClientCreateModelSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="id",
        read_only=False,
        # validators=[UniqueValidator(queryset=User.objects.all())],  # Defined validation in validate() method
        queryset=User.objects.filter(
            Q(is_staff=False) & Q(is_superuser=False) & Q(is_staff=False)))

    thumbnail_link = serializers.ImageField(validators=[validate_image_size])

    class Meta:
        model = Client
        fields = "__all__"  # Not used, if exclude is used (exclude= all-exclude)
        unique_together = ("id", "user")

    def to_representation(self, instance):  # Forms dictionary with response fields (fields-keys can be added)
        representation = super().to_representation(instance)
        representation["user_full_name"] = instance.user.full_name
        return representation

    def get_fields(self):
        fields = super().get_fields()

        try:
            current_user_id = self.context['request'].user.id
            fields["client_creator"].queryset = User.objects.filter(id=current_user_id)
            return fields
        except (ValueError, Exception) as error:
            print(gettext_lazy(EXCEPTION_INFO(error)))

        return fields


    def validate_thumbnail_link(self, value):
        # Model field defined validator intercepts value before validation in serializer
        return value


    def validate(self, attrs):
        attrs = super().validate(attrs)

        user_attr = attrs.get("user")
        client_creator_attr = attrs.get("client_creator")

        error_messages = []

        if not user_attr:
            error_messages.append(USER_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(USER_REQUIRED))

        if not client_creator_attr:
            error_messages.append(CLIENT_CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CLIENT_CREATOR_REQUIRED))

        if Client.objects.filter(user=user_attr).exists():
            error_messages.append(CLIENT_WITH_THIS_USER_ALREADY_EXISTS_MSG)
            # raise serializers.ValidationError(
            #     gettext_lazy(CLIENT_WITH_THIS_USER_ALREADY_EXISTS_MSG))

        if error_messages:
            ERROR_MESSAGES_STR = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(ERROR_MESSAGES_STR))

        return attrs
