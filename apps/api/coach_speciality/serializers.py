from rest_framework import serializers, request

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_non_front import EXCEPTION_INFO

from apps.api.messages_api.messages_errors import (CREATOR_REQUIRED,
                                                   COACH_SPECIALITY_REQUIRED,
                                                   COACH_SPECIALITY_EXISTS)

from apps.api.coach_speciality.models import CoachSpeciality
from apps.api.user.models import User



class CoachSpecialityAllFieldsModelSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="full_name",
                                           read_only=True)

    class Meta:
        model = CoachSpeciality
        # fields = "__all__"
        fields = ["id",
                  "name",
                  "description",
                  "created_at",
                  "updated_at",
                  "creator",
                  ]

class CoachSpecialityCreateModelSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="id",
                                           read_only=False,
                                           queryset=User.objects.all())

    class Meta:
        model = CoachSpeciality
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
            error_messages.append(COACH_SPECIALITY_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(COACH_SPECIALITY_REQUIRED))

        if not creator_in_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))

        if CoachSpeciality.objects.filter(name=name_in_attr).exists():
            error_messages.append(COACH_SPECIALITY_EXISTS)
            # raise serializers.ValidationError(
            #     gettext_lazy(COACH_SPECIALITY_EXISTS))

        if error_messages:
            error_messages_str = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(error_messages_str))

        return attrs



class CoachSpecialityRetrieveUpdateDeleteModelSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="id",
                                           read_only=False,
                                           queryset=User.objects.all())

    class Meta:
        model = CoachSpeciality
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
            error_messages.append(COACH_SPECIALITY_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(COACH_SPECIALITY_REQUIRED))

        if not creator_in_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))


        coach_speciality_id_view_passed_req_param = (
            self.context.get("coach_speciality_id"))

        old_coach_speciality_name = CoachSpeciality.objects.get(
            id=coach_speciality_id_view_passed_req_param).name

        new_coach_speciality_name = attrs.get("name")

        if new_coach_speciality_name != old_coach_speciality_name:
            if CoachSpeciality.objects.filter(
                    name=new_coach_speciality_name).exists():
                error_messages.append(COACH_SPECIALITY_EXISTS)
                # raise serializers.ValidationError(
                #     gettext_lazy(COACH_SPECIALITY_EXISTS))


        if error_messages:
            error_messages_str = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(error_messages_str))

        return attrs
