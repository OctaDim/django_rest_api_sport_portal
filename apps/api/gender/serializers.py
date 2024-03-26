from rest_framework import serializers, request

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_non_front import EXCEPTION_INFO

from apps.api.messages_api.messages_errors import (CREATOR_REQUIRED,
                                                   GENDER_REQUIRED,
                                                   GENDER_EXISTS)

from apps.api.gender.models import Gender
from apps.api.user.models import User



class GenderAllFieldsModelSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="full_name",
                                           read_only=True)

    class Meta:
        model = Gender
        # fields = "__all__"
        fields = ["id",
                  "name",
                  "created_at",
                  "updated_at",
                  "creator",
                  ]

class GenderCreateModelSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="id",
                                           read_only=False,
                                           queryset=User.objects.all())

    class Meta:
        model = Gender
        # fields = "__all__"
        fields = ["id",
                  "name",
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
            error_messages.append(GENDER_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(GENDER_REQUIRED))

        if not creator_in_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))

        if Gender.objects.filter(name=name_in_attr).exists():
            error_messages.append(GENDER_EXISTS)
            # raise serializers.ValidationError(
            #     gettext_lazy(GENDER_EXISTS))

        if error_messages:
            error_messages_str = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(error_messages_str))

        return attrs



class GenderRetrieveUpdateDeleteModelSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="id",
                                           read_only=False,
                                           queryset=User.objects.all())

    class Meta:
        model = Gender
        # fields = "__all__"
        fields = ["id",
                  "name",
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
            error_messages.append(GENDER_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(GENDER_REQUIRED))

        if not creator_in_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))


        gender_id_view_passed_req_param = (
            self.context.get("gender_id"))

        old_gender_name = Gender.objects.get(
            id=gender_id_view_passed_req_param).name

        new_gender_name = attrs.get("name")

        if new_gender_name != old_gender_name:
            if Gender.objects.filter(
                    name=new_gender_name).exists():
                error_messages.append(GENDER_EXISTS)
                # raise serializers.ValidationError(
                #     gettext_lazy(GENDER_EXISTS))


        if error_messages:
            error_messages_str = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(error_messages_str))

        return attrs
