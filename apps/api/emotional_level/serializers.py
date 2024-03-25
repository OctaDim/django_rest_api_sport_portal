from rest_framework import serializers, request
from rest_framework.validators import UniqueValidator

from django.utils.translation import gettext_lazy

from django.db.models import Q

from apps.api.messages_api.messages_non_front import EXCEPTION_INFO

from apps.api.messages_api.messages_actions import (
    ENTER_POSITIVE_FLOAT_OR_INT_NUMBER, ENTER_INTEGER_NUMBER)

from apps.api.messages_api.messages_errors import (
    EMOTIONAL_LEVEL_NAME_REQUIRED,
    EMOTIONAL_LEVEL_VALUE_REQUIRED,
    CREATOR_REQUIRED,
    EMOTIONAL_LEVEL_VALUE_EXISTS,
    EMOTIONAL_LEVEL_NAME_EXISTS,
    NOT_INTEGER_NUMBER,
    LEVEL_VALUE_MIN_LIMIT,
    LEVEL_VALUE_MAX_LIMIT
)

from apps.api.emotional_level.models import EmotionalLevel
from apps.api.user.models import User

from apps.api.user.serializers import UsersAllFieldsNoPermissionsSerializer

from apps.api.emotional_level.settings import (EMOTIONAL_LEVEL_VALUE_MIN_LIMIT,
                                               EMOTIONAL_LEVEL_VALUE_MAX_LIMIT)

from apps.api.utils.utils import get_abs_float_from_str_or_number, get_integer_from_str_or_number



class EmotionalLevelAllFieldsModelSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="full_name",
                                           read_only=True)

    class Meta:
        model = EmotionalLevel
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

class EmotionalLevelCreateModelSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="id",
                                           read_only=False,
                                           queryset=User.objects.all())

    value = serializers.CharField(
        max_length=10,
        required=True,
        help_text=gettext_lazy(
            f"{ENTER_INTEGER_NUMBER} in range "
            f"[{EMOTIONAL_LEVEL_VALUE_MIN_LIMIT} : "
            f"{EMOTIONAL_LEVEL_VALUE_MAX_LIMIT}]"))

    class Meta:
        model = EmotionalLevel
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
            error_messages.append(EMOTIONAL_LEVEL_NAME_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(EMOTIONAL_LEVEL_NAME_REQUIRED))

        if EmotionalLevel.objects.filter(name=level_name_in_attr).exists():
            error_messages.append(EMOTIONAL_LEVEL_NAME_EXISTS)
            # raise serializers.ValidationError(
            #     gettext_lazy(EMOTIONAL_LEVEL_NAME_EXISTS))

        if not creator_in_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))

        if not level_value_in_attr:
            error_messages.append(EMOTIONAL_LEVEL_VALUE_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(EMOTIONAL_LEVEL_VALUE_REQUIRED))

        if not level_value_in_attr:
            attrs["value"] = None  # To replace empty "" str value with None valid for db FloatField
        else:
            converted_value = get_integer_from_str_or_number(level_value_in_attr)

            if not converted_value:
                error_messages.append(NOT_INTEGER_NUMBER(
                    field_name="value", field_value=level_value_in_attr))
                # raise serializers.ValidationError(gettext_lazy(
                #     NOT_POSITIVE_FLOAT_OR_INT("value", level_value_in_attr)))
            else:
                min_value_limit = EMOTIONAL_LEVEL_VALUE_MIN_LIMIT
                max_value_limit = EMOTIONAL_LEVEL_VALUE_MAX_LIMIT

                if converted_value < min_value_limit:
                    error_messages.append(LEVEL_VALUE_MIN_LIMIT(
                        value=converted_value, min_limit=min_value_limit))
                    # raise serializers.ValidationError(gettext_lazy(
                    #     LEVEL_VALUE_MIN_LIMIT(converted_value, min_value_limit)))

                elif converted_value > max_value_limit:
                    error_messages.append(LEVEL_VALUE_MAX_LIMIT(
                        value=converted_value, max_limit=max_value_limit))
                    # raise serializers.ValidationError(gettext_lazy(
                    #     LEVEL_VALUE_MAX_LIMIT(converted_value, max_value_limit)))

                if EmotionalLevel.objects.filter(value=converted_value).exists():
                    error_messages.append(EMOTIONAL_LEVEL_VALUE_EXISTS)
                    # raise serializers.ValidationError(
                    #     gettext_lazy(EMOTIONAL_LEVEL_VALUE_EXISTS))

                else:
                    attrs["value"] = converted_value  # Replacing by the value converted to the valid formant

        if error_messages:
            error_messages_str = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(error_messages_str))

        return attrs



class EmotionalLevelRetrieveUpdateDeleteModelSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="id",
                                           read_only=False,
                                           queryset=User.objects.all())

    value = serializers.CharField(
        max_length=10,
        required=True,
        help_text=gettext_lazy(
            f"{ENTER_INTEGER_NUMBER} in range "
            f"[{EMOTIONAL_LEVEL_VALUE_MIN_LIMIT} : "
            f"{EMOTIONAL_LEVEL_VALUE_MAX_LIMIT}]"))

    class Meta:
        model = EmotionalLevel
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
            error_messages.append(EMOTIONAL_LEVEL_NAME_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(EMOTIONAL_LEVEL_NAME_REQUIRED))


        emotional_level_id_view_passed_req_param = (
                                    self.context.get("emotional_level_id"))

        old_emotional_level_name = EmotionalLevel.objects.get(
            id=emotional_level_id_view_passed_req_param).name

        new_emotional_level_name = attrs.get("name")

        if new_emotional_level_name != old_emotional_level_name:
            if EmotionalLevel.objects.filter(
                    name=new_emotional_level_name).exists():
                error_messages.append(EMOTIONAL_LEVEL_NAME_EXISTS)
                # raise serializers.ValidationError(
                #     gettext_lazy(EMOTIONAL_LEVEL_NAME_EXISTS))


        if not creator_in_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))

        if not level_value_in_attr:
            error_messages.append(EMOTIONAL_LEVEL_VALUE_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(EMOTIONAL_LEVEL_VALUE_REQUIRED))

        if not level_value_in_attr:
            attrs["value"] = None  # To replace empty "" str value with None valid for db FloatField
        else:
            converted_value = get_integer_from_str_or_number(level_value_in_attr)

            if not converted_value:
                error_messages.append(NOT_INTEGER_NUMBER(
                    field_name="value", field_value=level_value_in_attr))
                # raise serializers.ValidationError(gettext_lazy(
                #     NOT_POSITIVE_FLOAT_OR_INT("value", level_value_in_attr)))
            else:
                min_value_limit = EMOTIONAL_LEVEL_VALUE_MIN_LIMIT
                max_value_limit = EMOTIONAL_LEVEL_VALUE_MAX_LIMIT

                if converted_value < min_value_limit:
                    error_messages.append(LEVEL_VALUE_MIN_LIMIT(
                        value=converted_value, min_limit=min_value_limit))
                    # raise serializers.ValidationError(gettext_lazy(
                    #     LEVEL_VALUE_MIN_LIMIT(converted_value, min_value_limit)))

                elif converted_value > max_value_limit:
                    error_messages.append(LEVEL_VALUE_MAX_LIMIT(
                        value=converted_value, max_limit=max_value_limit))
                    # raise serializers.ValidationError(gettext_lazy(
                    #     LEVEL_VALUE_MAX_LIMIT(converted_value, max_value_limit)))


                emotional_level_id_view_passed_req_param = (
                    self.context.get("emotional_level_id"))

                old_emotional_level_value = EmotionalLevel.objects.get(
                    id=emotional_level_id_view_passed_req_param).value

                new_emotional_level_value = attrs.get("value")

                if new_emotional_level_value != old_emotional_level_value:
                    if EmotionalLevel.objects.filter(
                            name=new_emotional_level_value).exists():
                        error_messages.append(EMOTIONAL_LEVEL_VALUE_EXISTS)
                        # raise serializers.ValidationError(
                        #     gettext_lazy(EMOTIONAL_LEVEL_VALUE_EXISTS))


                else:
                    attrs["value"] = converted_value  # Replacing by the value converted to the valid formant

        if error_messages:
            error_messages_str = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(error_messages_str))

        return attrs
