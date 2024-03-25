from rest_framework import serializers, request
from rest_framework.validators import UniqueValidator

from django.utils.translation import gettext_lazy

from django.db.models import Q

from apps.api.messages_api.messages_non_front import EXCEPTION_INFO

from apps.api.messages_api.messages_actions import (
    ENTER_POSITIVE_FLOAT_OR_INT_NUMBER, ENTER_INTEGER_NUMBER)

from apps.api.messages_api.messages_errors import (
                                        SATISFACTION_LEVEL_NAME_REQUIRED,
                                        SATISFACTION_LEVEL_VALUE_REQUIRED,
                                        CREATOR_REQUIRED,
                                        SATISFACTION_LEVEL_VALUE_EXISTS,
                                        SATISFACTION_LEVEL_NAME_EXISTS,
                                        NOT_INTEGER_NUMBER,
                                        LEVEL_VALUE_MIN_LIMIT,
                                        LEVEL_VALUE_MAX_LIMIT
                                        )

from apps.api.self_satisfaction_level.models import SelfSatisfactionLevel
from apps.api.user.models import User

from apps.api.user.serializers import UsersAllFieldsNoPermissionsSerializer

from apps.api.utils.utils import (get_integer_from_str_or_number,
                                  number_or_str_to_int)

from apps.api.self_satisfaction_level.settings import (
                                    SATISFACTION_LEVEL_VALUE_MIN_LIMIT,
                                    SATISFACTION_LEVEL_VALUE_MAX_LIMIT)

from apps.api.utils.utils import get_integer_from_str_or_number



class SatisfactionLevelAllFieldsModelSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="full_name",
                                           read_only=True)

    class Meta:
        model = SelfSatisfactionLevel
        # fields = "__all__"
        fields = ["id",
                  "icon_link",
                  "value",
                  "name",
                  "description",
                  "created_at",
                  "updated_at",
                  "creator",
                  ]

class SatisfactionLevelCreateModelSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="id",
                                           read_only=False,
                                           queryset=User.objects.all())

    value = serializers.CharField(
        max_length=10,
        required=True,
        help_text=gettext_lazy(
            f"{ENTER_INTEGER_NUMBER} in range "
            f"[{SATISFACTION_LEVEL_VALUE_MIN_LIMIT} : "
            f"{SATISFACTION_LEVEL_VALUE_MAX_LIMIT}]"))

    class Meta:
        model = SelfSatisfactionLevel
        # fields = "__all__"
        fields = ["id",
                  "icon_link",
                  "value",
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

        level_name_in_attr = attrs.get("name")
        level_value_in_attr = attrs.get("value")
        creator_in_attr = attrs.get("creator")

        if not level_name_in_attr:
            error_messages.append(SATISFACTION_LEVEL_NAME_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(SATISFACTION_LEVEL_NAME_REQUIRED))

        if SelfSatisfactionLevel.objects.filter(name=level_name_in_attr).exists():
            error_messages.append(SATISFACTION_LEVEL_NAME_EXISTS)
            # raise serializers.ValidationError(
            #     gettext_lazy(SATISFACTION_LEVEL_NAME_EXISTS))

        if not creator_in_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))

        if not level_value_in_attr:
            error_messages.append(SATISFACTION_LEVEL_VALUE_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(SATISFACTION_LEVEL_VALUE_REQUIRED))

        if not level_value_in_attr:
            attrs["value"] = None  # To replace empty "" str value with None valid for db FloatField
        else:
            int_converted_value = get_integer_from_str_or_number(level_value_in_attr)

            if not int_converted_value:
                error_messages.append(NOT_INTEGER_NUMBER(
                    field_name="value", field_value=level_value_in_attr))
                # raise serializers.ValidationError(gettext_lazy(
                #     NOT_POSITIVE_FLOAT_OR_INT("value", level_value_in_attr)))
            else:
                min_value_limit = number_or_str_to_int(SATISFACTION_LEVEL_VALUE_MIN_LIMIT)
                max_value_limit = number_or_str_to_int(SATISFACTION_LEVEL_VALUE_MAX_LIMIT)

                if int_converted_value < min_value_limit:
                    error_messages.append(LEVEL_VALUE_MIN_LIMIT(
                        value=int_converted_value, min_limit=min_value_limit))
                    # raise serializers.ValidationError(gettext_lazy(
                    #     LEVEL_VALUE_MIN_LIMIT(int_converted_value, min_value_limit)))

                elif int_converted_value > max_value_limit:
                    error_messages.append(LEVEL_VALUE_MAX_LIMIT(
                        value=int_converted_value, max_limit=max_value_limit))
                    # raise serializers.ValidationError(gettext_lazy(
                    #     LEVEL_VALUE_MAX_LIMIT(int_converted_value, max_value_limit)))

                if SelfSatisfactionLevel.objects.filter(value=int_converted_value).exists():
                    error_messages.append(SATISFACTION_LEVEL_VALUE_EXISTS)
                    # raise serializers.ValidationError(
                    #     gettext_lazy(SATISFACTION_LEVEL_VALUE_EXISTS))

                attrs["value"] = int_converted_value  # Replacing by the value converted to the valid formant

        if error_messages:
            error_messages_str = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(error_messages_str))

        return attrs



class SatisfactionLevelRetrieveUpdateDeleteModelSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="id",
                                           read_only=False,
                                           queryset=User.objects.all())

    value = serializers.CharField(
        max_length=10,
        required=True,
        help_text=gettext_lazy(
            f"{ENTER_INTEGER_NUMBER} in range "
            f"[{SATISFACTION_LEVEL_VALUE_MIN_LIMIT} : "
            f"{SATISFACTION_LEVEL_VALUE_MAX_LIMIT}]"))

    class Meta:
        model = SelfSatisfactionLevel
        # fields = "__all__"
        fields = ["id",
                  "icon_link",
                  "value",
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

        level_name_in_attr = attrs.get("name")
        level_value_in_attr = attrs.get("value")
        creator_in_attr = attrs.get("creator")

        if not level_name_in_attr:
            error_messages.append(SATISFACTION_LEVEL_NAME_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(SATISFACTION_LEVEL_NAME_REQUIRED))


        satisfaction_level_id_view_passed_req_param = (
            self.context.get("satisfaction_level_id"))

        old_satisfaction_level_name = SelfSatisfactionLevel.objects.get(
            id=satisfaction_level_id_view_passed_req_param).name

        new_satisfaction_level_name = attrs.get("name")

        if new_satisfaction_level_name != old_satisfaction_level_name:
            if SelfSatisfactionLevel.objects.filter(
                    name=new_satisfaction_level_name).exists():
                error_messages.append(SATISFACTION_LEVEL_NAME_EXISTS)
                # raise serializers.ValidationError(
                #     gettext_lazy(SATISFACTION_LEVEL_NAME_EXISTS))


        if not creator_in_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))

        if not level_value_in_attr:
            error_messages.append(SATISFACTION_LEVEL_VALUE_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(SATISFACTION_LEVEL_VALUE_REQUIRED))

        if not level_value_in_attr:
            attrs["value"] = None  # To replace empty "" str value with None valid for db FloatField
        else:
            int_converted_value = get_integer_from_str_or_number(level_value_in_attr)

            if not int_converted_value:
                error_messages.append(NOT_INTEGER_NUMBER(
                    field_name="value", field_value=level_value_in_attr))
                # raise serializers.ValidationError(gettext_lazy(
                #     NOT_POSITIVE_FLOAT_OR_INT("value", level_value_in_attr)))

            else:
                min_value_limit = number_or_str_to_int(SATISFACTION_LEVEL_VALUE_MIN_LIMIT)
                max_value_limit = number_or_str_to_int(SATISFACTION_LEVEL_VALUE_MAX_LIMIT)

                if int_converted_value < min_value_limit:
                    error_messages.append(LEVEL_VALUE_MIN_LIMIT(
                        value=int_converted_value, min_limit=min_value_limit))
                    # raise serializers.ValidationError(gettext_lazy(
                    #     LEVEL_VALUE_MIN_LIMIT(int_converted_value, min_value_limit)))

                if int_converted_value > max_value_limit:
                    error_messages.append(LEVEL_VALUE_MAX_LIMIT(
                        value=int_converted_value, max_limit=max_value_limit))
                    # raise serializers.ValidationError(gettext_lazy(
                    #     LEVEL_VALUE_MAX_LIMIT(int_converted_value, max_value_limit)))


                satisfaction_level_id_view_passed_req_param = (
                    self.context.get("satisfaction_level_id"))

                old_satisfaction_level_value = SelfSatisfactionLevel.objects.get(
                    id=satisfaction_level_id_view_passed_req_param).value

                new_satisfaction_level_value = int_converted_value

                if new_satisfaction_level_value != old_satisfaction_level_value:
                    if SelfSatisfactionLevel.objects.filter(
                                value=new_satisfaction_level_value).exists():
                        error_messages.append(SATISFACTION_LEVEL_VALUE_EXISTS)
                        # raise serializers.ValidationError(
                        #     gettext_lazy(SATISFACTION_LEVEL_VALUE_EXISTS))

                attrs["value"] = int_converted_value  # Replacing by the value converted to the valid formant

        if error_messages:
            error_messages_str = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(error_messages_str))
        return attrs
