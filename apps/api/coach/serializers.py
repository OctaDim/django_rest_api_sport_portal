from rest_framework import serializers, request
from rest_framework.validators import UniqueValidator

from django.utils.translation import gettext_lazy

from django.db.models import Q

from apps.api.messages_api.messages_non_front import EXCEPTION_INFO

from apps.api.messages_api.messages_errors import (
    USER_REQUIRED,
    COACH_CREATOR_REQUIRED,
    COACH_WITH_USER_ALREADY_EXISTS,
                                    )

from apps.api.coach.models import Coach
from apps.api.user.models import User
from apps.api.coach_speciality.models import CoachSpeciality
from apps.api.country.models import Country
from apps.api.gender.models import Gender

from apps.api.user.serializers import UsersAllFieldsNoPermissionsSerializer

from apps.api.coach.validators import validate_image_size



class CoachAllFieldsModelSerializer(serializers.ModelSerializer):
    user = UsersAllFieldsNoPermissionsSerializer(read_only=True)

    coach_creator = serializers.SlugRelatedField(slug_field="full_name",
                                                  read_only=True)

    coach_speciality = serializers.SlugRelatedField(slug_field="name",
                                                    read_only=True)

    country = serializers.SlugRelatedField(slug_field="name",
                                           read_only=True)

    gender = serializers.SlugRelatedField(slug_field="name",
                                          read_only=True)

    class Meta:
        model = Coach
        # fields = "__all__"
        fields = ["id",
                  "user",
                  "thumbnail_link",
                  "coach_speciality",
                  "first_name",
                  "last_name",
                  "phone",
                  "address",
                  "birth_date",
                  "bibliography",
                  "note",
                  "created_at",
                  "updated_at",
                  "country",
                  "gender",
                  "coach_creator",
                  ]



class CoachCreateModelSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="id",
        read_only=False,
        # validators=[UniqueValidator(queryset=User.objects.all())],  # Defined validation in validate() method
        queryset=User.objects.filter(
            Q(is_staff=True) & Q(is_trainer=True)
        )
    )

    coach_speciality = serializers.SlugRelatedField(
                                slug_field="name",
                                read_only=False,
                                queryset=CoachSpeciality.objects.all())

    country = serializers.SlugRelatedField(slug_field="name",
                                           read_only=False,
                                           queryset=Country.objects.all())

    gender = serializers.SlugRelatedField(slug_field="name",
                                          read_only=False,
                                          queryset=Gender.objects.all())

    class Meta:
        model = Coach
        unique_together = ("id", "user")
        # fields = "__all__"  # Not used, if exclude is used (exclude= all-exclude)
        fields = ["id",
                  "user",
                  "thumbnail_link",
                  "coach_speciality",
                  "first_name",
                  "last_name",
                  "phone",
                  "address",
                  "birth_date",
                  "bibliography",
                  "note",
                  "created_at",
                  "updated_at",
                  "country",
                  "gender",
                  "coach_creator",
                  ]

    def to_representation(self, instance):  # Forms dictionary with response fields (fields-keys can be added)
        representation = super().to_representation(instance)
        representation["coach_creator_full_name"] = instance.coach_creator.full_name
        representation["user_full_name"] = instance.user.full_name
        representation["user_is_active"] = instance.user.is_active
        representation["user_is_verified"] = instance.user.is_verified
        representation["user_is_staff"] = instance.user.is_staff
        representation["user_is_trainer"] = instance.user.is_trainer
        representation["user_is_superuser"] = instance.user.is_superuser

        return representation


    def get_fields(self):
        fields = super().get_fields()

        try:
            current_user_id = self.context["request"].user.id
            fields["coach_creator"].queryset = User.objects.filter(id=current_user_id)
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
        coach_creator_attr = attrs.get("coach_creator")

        error_messages = []

        if not user_attr:
            error_messages.append(USER_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(USER_REQUIRED))

        if not coach_creator_attr:
            error_messages.append(COACH_CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(COACH_CREATOR_REQUIRED))

        if Coach.objects.filter(user=user_attr).exists():
            error_messages.append(COACH_WITH_USER_ALREADY_EXISTS)
            # raise serializers.ValidationError(
            #     gettext_lazy(COACH_WITH_USER_ALREADY_EXISTS))

        if error_messages:
            ERROR_MESSAGES_STR = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(ERROR_MESSAGES_STR))

        return attrs



class CoachRetrieveUpdateDeleteModelSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="id",
        read_only=False,
        # validators=[UniqueValidator(queryset=User.objects.all())],  # Defined validation in validate() method
        queryset=User.objects.filter(
            Q(is_staff=True) & Q(is_trainer=True)
        )
    )

    user_is_active = serializers.BooleanField(write_only=True,  # IMPORTANT: write_only=True if no model field
                                              allow_null=False,
                                              initial=True,
                                              )

    coach_speciality = serializers.SlugRelatedField(
                                slug_field="name",
                                read_only=False,
                                queryset=CoachSpeciality.objects.all())

    country = serializers.SlugRelatedField(slug_field="name",
                                           read_only=False,
                                           queryset=Country.objects.all())

    gender = serializers.SlugRelatedField(slug_field="name",
                                          read_only=False,
                                          queryset=Gender.objects.all())

    class Meta:
        model = Coach
        fields = "__all__"  # Not used, if exclude is used (exclude= all-exclude)
        unique_together = ("id", "user")


    def to_representation(self, instance):  # Forms dictionary with response fields (fields-keys can be added)
        representation = super().to_representation(instance)
        representation["coach_creator_full_name"] = instance.coach_creator.full_name
        representation["user_full_name"] = instance.user.full_name
        representation["user_is_active"] = instance.user.is_active
        representation["user_is_verified"] = instance.user.is_verified
        representation["user_is_staff"] = instance.user.is_staff
        representation["user_is_trainer"] = instance.user.is_trainer
        representation["user_is_superuser"] = instance.user.is_superuser
        return representation


    def get_fields(self):
        fields = super().get_fields()

        try:
            current_user_id = self.context['request'].user.id
            fields["coach_creator"].queryset = User.objects.filter(id=current_user_id)
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
        coach_creator_in_attrs = attrs.get("coach_creator")

        if not user_in_attrs:
            error_messages.append(USER_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(USER_REQUIRED))

        if not coach_creator_in_attrs:
            error_messages.append(COACH_CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(COACH_CREATOR_REQUIRED))

        coach_id_from_view_passed_request_param = self.context.get("coach_id")
        old_user_id_in_coach = Coach.objects.get(
                        id=coach_id_from_view_passed_request_param).user.id
        new_user_id_in_coach = attrs.get("user").id
        user_in_attrs = attrs.get("user")

        if new_user_id_in_coach != old_user_id_in_coach:
            if Coach.objects.filter(user=user_in_attrs):
                error_messages.append(COACH_WITH_USER_ALREADY_EXISTS)
                # raise serializers.ValidationError(
                #     gettext_lazy(COACH_WITH_USER_ALREADY_EXISTS))

        if error_messages:
            error_messages_str = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(error_messages_str))

        attrs.setdefault("user_is_active", False)  # If None, should be False, fixed django bug Boolean field None value

        return attrs
