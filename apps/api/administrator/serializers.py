from rest_framework import serializers, request
from rest_framework.validators import UniqueValidator

from django.utils.translation import gettext_lazy

from django.db.models import Q

from apps.api.messages_api.messages_non_front import EXCEPTION_INFO

from apps.api.messages_api.messages_errors import (
                                            USER_REQUIRED,
                                            ADMINISTRATOR_CREATOR_REQUIRED,
                                            ADMINISTRATOR_WITH_USER_ALREADY_EXISTS,
                                            )

from apps.api.administrator.models import Administrator
from apps.api.user.models import User

from apps.api.user.serializers import UsersAllFieldsNoPermissionsSerializer

from apps.api.administrator.validators import validate_image_size



class AdministratorAllFieldsModelSerializer(serializers.ModelSerializer):
    user = UsersAllFieldsNoPermissionsSerializer(read_only=True)

    administrator_creator = serializers.SlugRelatedField(slug_field="full_name",
                                                  read_only=True)

    class Meta:
        model = Administrator
        fields = "__all__"



class AdministratorCreateModelSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="id",
        read_only=False,
        # validators=[UniqueValidator(queryset=User.objects.all())],  # Defined validation in validate() method
        queryset=User.objects.filter(
            Q(is_staff=False) & Q(is_superuser=False) & Q(is_staff=False)))

    class Meta:
        model = Administrator
        fields = "__all__"  # Not used, if exclude is used (exclude= all-exclude)
        unique_together = ("id", "user")


    def to_representation(self, instance):  # Forms dictionary with response fields (fields-keys can be added)
        representation = super().to_representation(instance)
        representation["administrator_creator_full_name"] = instance.administrator_creator.full_name
        representation["user_is_active"] = instance.user.is_active
        representation["user_full_name"] = instance.user.full_name

        return representation


    def get_fields(self):
        fields = super().get_fields()

        try:
            current_user_id = self.context["request"].user.id
            fields["administrator_creator"].queryset = User.objects.filter(id=current_user_id)
            return fields
        except (ValueError, Exception) as error:
            print(gettext_lazy(EXCEPTION_INFO(error)))

        return fields


    # def validate_thumbnail_link(self, value):
    #     # Model field defined validator intercepts value before validation in serializer
    #     return value


    def validate(self, attrs):
        attrs = super().validate(attrs)

        user_attr = attrs.get("user")
        administrator_creator_attr = attrs.get("administrator_creator")

        error_messages = []

        if not user_attr:
            error_messages.append(USER_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(USER_REQUIRED))

        if not administrator_creator_attr:
            error_messages.append(ADMINISTRATOR_CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(ADMINISTRATOR_CREATOR_REQUIRED))

        if Administrator.objects.filter(user=user_attr).exists():
            error_messages.append(ADMINISTRATOR_WITH_USER_ALREADY_EXISTS)
            # raise serializers.ValidationError(
            #     gettext_lazy(ADMINISTRATOR_WITH_USER_ALREADY_EXISTS))

        if error_messages:
            ERROR_MESSAGES_STR = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(ERROR_MESSAGES_STR))

        return attrs



class AdministratorRetrieveUpdateDeleteModelSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="id",
        read_only=False,
        # validators=[UniqueValidator(queryset=User.objects.all())],  # Defined validation in validate() method
        queryset=User.objects.filter(
            Q(is_staff=False) & Q(is_superuser=False) & Q(is_staff=False)))

    user_is_active = serializers.BooleanField(write_only=True,  # IMPORTANT: write_only=True if no model field
                                              allow_null=False,
                                              initial=True,
                                              )

    class Meta:
        model = Administrator
        fields = "__all__"  # Not used, if exclude is used (exclude= all-exclude)
        unique_together = ("id", "user")
        # fields = ["id", "user", "administrator_creator", "user_is_active"]


    def to_representation(self, instance):  # Forms dictionary with response fields (fields-keys can be added)
        representation = super().to_representation(instance)
        representation["administrator_creator_full_name"] = instance.administrator_creator.full_name
        representation["user_is_active"] = instance.user.is_active
        representation["user_full_name"] = instance.user.full_name
        return representation


    def get_fields(self):
        fields = super().get_fields()

        try:
            current_user_id = self.context['request'].user.id
            fields["administrator_creator"].queryset = User.objects.filter(id=current_user_id)
            return fields
        except (ValueError, Exception) as error:
            print(gettext_lazy(EXCEPTION_INFO(error)))

        return fields


    # def validate_thumbnail_link(self, value):
    #     # Model field defined validator intercepts value before validation in serializer
    #     return value


    def validate(self, attrs, *args, **kwargs):
        attrs = super().validate(attrs)

        error_messages = []

        user_in_attrs = attrs.get("user")
        administrator_creator_in_attrs = attrs.get("administrator_creator")

        if not user_in_attrs:
            error_messages.append(USER_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(USER_REQUIRED))

        if not administrator_creator_in_attrs:
            error_messages.append(ADMINISTRATOR_CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(ADMINISTRATOR_CREATOR_REQUIRED))

        administrator_id_from_view_passed_request_param = self.context.get("administrator_id")
        old_user_id_in_administrator = Administrator.objects.get(
                        id=administrator_id_from_view_passed_request_param).user.id
        new_user_id_in_administrator = attrs.get("user").id
        user_in_attrs = attrs.get("user")

        if new_user_id_in_administrator != old_user_id_in_administrator:
            if Administrator.objects.filter(user=user_in_attrs):
                error_messages.append(ADMINISTRATOR_WITH_USER_ALREADY_EXISTS)
                # raise serializers.ValidationError(
                #     gettext_lazy(ADMINISTRATOR_WITH_USER_ALREADY_EXISTS))

        if error_messages:
            error_messages_str = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(error_messages_str))

        attrs.setdefault("user_is_active", False)  # If None, should be False, fixed django bug Boolean field None value

        return attrs
