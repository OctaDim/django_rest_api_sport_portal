from rest_framework import serializers, request
from rest_framework.validators import UniqueValidator

from django.utils.translation import gettext_lazy

from django.db.models import Q

from apps.api.messages_api.messages_non_front import EXCEPTION_INFO

from apps.api.messages_api.messages_actions import ENTER_POSITIVE_FLOAT_OR_INT_NUMBER

from apps.api.messages_api.messages_errors import (
                                        GROUP_CLIENT_REQUIRED,
                                        SELF_SATISFACTION_LEVEL_REQUIRED,
                                        EMOTIONAL_LEVEL_REQUIRED,
                                        CHECK_POINT_DATE_REQUIRED,
                                        CREATOR_REQUIRED,
                                        GROUP_CLIENT_DATE_EXISTS,
                                        NOT_POSITIVE_FLOAT_OR_INT,
                                        )

from apps.api.group_client_progress.models import GroupClientProgress
from apps.api.training_group.models import TrainingGroup
from apps.api.group_many_client.models import GroupManyClient
from apps.api.self_satisfaction_level.models import SelfSatisfactionLevel
from apps.api.emotional_level.models import EmotionalLevel
from apps.api.user.models import User

from apps.api.utils.utils import get_abs_float_from_str_or_number

from apps.api.user.serializers import UsersAllFieldsNoPermissionsSerializer



class GroupClientProgressAllFieldsModelSerializer(serializers.ModelSerializer):
    group_many_client = serializers.SlugRelatedField(slug_field="full_name",
                                                     read_only=True)

    self_satisfaction_level = serializers.SerializerMethodField()

    emotional_level = serializers.SerializerMethodField()

    task_completed = serializers.BooleanField(read_only=True,
                                              initial=False)

    creator = serializers.SlugRelatedField(slug_field="full_name",
                                           read_only=True)

    class Meta:
        model = GroupClientProgress
        # fields = "__all__"
        fields = ["id",
                  "group_many_client",
                  "self_satisfaction_level",
                  "emotional_level",
                  "task_completed",
                  "check_point_date",
                  "current_weight",
                  "current_breast",
                  "current_shoulders",
                  "current_waist",
                  "current_hips",
                  "current_height",
                  "description",
                  "note",
                  "created_at",
                  "updated_at",
                  "creator",
                  ]

    def get_self_satisfaction_level(self, obj):
        self_satisfaction_level = {
            "self_satisfaction_level_str": str(obj.self_satisfaction_level),
            "self_satisfaction_level_id": obj.self_satisfaction_level.id,
            "self_satisfaction_level_value": obj.self_satisfaction_level.value,
            "self_satisfaction_level_name": obj.self_satisfaction_level.name,
            "self_satisfaction_level_full_name": obj.self_satisfaction_level.full_name}
        return self_satisfaction_level


    def get_emotional_level(self, obj):
        emotional_level = {
            "emotional_level_str": str(obj.emotional_level),
            "emotional_level_id": obj.emotional_level.id,
            "emotional_level_value": obj.emotional_level.value,
            "emotional_level_name": obj.emotional_level.name,
            "emotional_level_full_name": obj.emotional_level.full_name}
        return emotional_level



class GroupClientProgressCreateModelSerializer(serializers.ModelSerializer):
    group_many_client = serializers.SlugRelatedField(
                                slug_field="id",
                                read_only=False,
                                queryset=GroupManyClient.objects.all())

    self_satisfaction_level = serializers.SlugRelatedField(
                                slug_field="id",
                                read_only=False,
                                queryset=SelfSatisfactionLevel.objects.all())

    emotional_level = serializers.SlugRelatedField(
                                slug_field="id",
                                read_only=False,
                                queryset=EmotionalLevel.objects.all())

    task_completed = serializers.BooleanField(read_only=False,
                                              initial=False)

    creator = serializers.SlugRelatedField(
                                        slug_field="id",
                                        read_only=False,
                                        queryset=User.objects.all())

    current_weight = serializers.CharField(
        max_length=10,
        allow_blank=True, allow_null=True,
        help_text=gettext_lazy(ENTER_POSITIVE_FLOAT_OR_INT_NUMBER))

    current_breast = serializers.CharField(
        max_length=10,
        allow_blank=True, allow_null=True,
        help_text=gettext_lazy(ENTER_POSITIVE_FLOAT_OR_INT_NUMBER))

    current_shoulders = serializers.CharField(
        max_length=10,
        allow_blank=True, allow_null=True,
        help_text=gettext_lazy(ENTER_POSITIVE_FLOAT_OR_INT_NUMBER))

    current_waist = serializers.CharField(
        max_length=10,
        allow_blank=True, allow_null=True,
        help_text=gettext_lazy(ENTER_POSITIVE_FLOAT_OR_INT_NUMBER))

    current_hips = serializers.CharField(
        max_length=10,
        allow_blank=True, allow_null=True,
        help_text=gettext_lazy(ENTER_POSITIVE_FLOAT_OR_INT_NUMBER))

    current_height = serializers.CharField(
        max_length=10,
        allow_blank=True, allow_null=True,
        help_text=gettext_lazy(ENTER_POSITIVE_FLOAT_OR_INT_NUMBER))

    class Meta:
        model = GroupClientProgress
        # fields = "__all__"
        fields = ["id",
                  "group_many_client",
                  "self_satisfaction_level",
                  "emotional_level",
                  "task_completed",
                  "check_point_date",
                  "current_weight",
                  "current_breast",
                  "current_shoulders",
                  "current_waist",
                  "current_hips",
                  "current_height",
                  "description",
                  "note",
                  "created_at",
                  "updated_at",
                  "creator",
                  ]

    def get_fields(self):
        fields = super().get_fields()

        fields["group_many_client"].queryset = GroupManyClient.objects.order_by(
            "training_group_id__training_group_code", # order by field, defined pk field and curr field
            "training_group_id__training_group_name", # order by field, defined pk field and curr field
            "client_id__user")                        # order by __str__, defined only pk field without curr field

        fields["self_satisfaction_level"].queryset = SelfSatisfactionLevel.objects.order_by(
            "-value", "name")

        fields["emotional_level"].queryset = EmotionalLevel.objects.order_by(
            "-value", "name")

        try:
            current_user_id = self.context["request"].user.id
            fields["creator"].queryset = User.objects.filter(id=current_user_id)
            return fields
        except (ValueError, Exception) as error:
            print(gettext_lazy(EXCEPTION_INFO(error)))
        return fields


    def to_representation(self, instance):  # Forms dictionary with response fields (fields-keys can be added)
        representation = super().to_representation(instance)
        representation["group_many_client"] = str(instance.group_many_client)
        representation["self_satisfaction_level"] = str(instance.self_satisfaction_level)
        representation["emotional_level"] = str(instance.emotional_level)
        representation["creator"] = str(instance.creator)

        representation["training_group_id"] = instance.group_many_client.training_group_id.id                    # Field
        representation["training_group_code"] = instance.group_many_client.training_group_id.training_group_code # Field
        representation["training_group_name"] = instance.group_many_client.training_group_id.training_group_name # Field
        representation["training_group_full_name"] = instance.group_many_client.training_group_id.full_name  # @Property
        representation["training_group_str"] = str(instance.group_many_client.training_group_id)             # __str__

        representation["client_id"] = instance.group_many_client.client_id.id
        representation["client_full_name"] = instance.group_many_client.client_id.full_name
        representation["client_str"] = str(instance.group_many_client.client_id)

        representation["self_satisfaction_level_id"] = instance.self_satisfaction_level.id
        representation["self_satisfaction_level_value"] = instance.self_satisfaction_level.value
        representation["self_satisfaction_level_name"] = instance.self_satisfaction_level.name
        representation["self_satisfaction_level_full_name"] = instance.self_satisfaction_level.full_name

        representation["emotional_level_id"] = instance.emotional_level.id
        representation["emotional_level_value"] = instance.emotional_level.value
        representation["emotional_level_name"] = instance.emotional_level.name
        representation["emotional_level_full_name"] = instance.emotional_level.full_name

        representation["creator_id"] = str(instance.creator.id)

        return representation

    def validate(self, attrs):
        attrs = super().validate(attrs)

        error_messages = []

        group_many_client_attr = attrs.get("group_many_client")
        if not group_many_client_attr:
            error_messages.append(GROUP_CLIENT_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(GROUP_CLIENT_REQUIRED))

        self_satisfaction_level_attr = attrs.get("self_satisfaction_level")
        if not self_satisfaction_level_attr:
            error_messages.append(SELF_SATISFACTION_LEVEL_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(SELF_SATISFACTION_LEVEL_REQUIRED))

        emotional_level_attr = attrs.get("emotional_level")
        if not emotional_level_attr:
            error_messages.append(EMOTIONAL_LEVEL_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(EMOTIONAL_LEVEL_REQUIRED))

        check_point_date_attr = attrs.get("check_point_date")
        if not check_point_date_attr:
            error_messages.append(CHECK_POINT_DATE_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CHECK_POINT_DATE_REQUIRED))

        creator_attr = attrs.get("creator")
        if not creator_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))

        float_fields_to_validate_names = ["current_weight",
                                          "current_breast",
                                          "current_shoulders",
                                          "current_waist",
                                          "current_hips",
                                          "current_height"]

        for field_name in float_fields_to_validate_names:
            field_value_attr = attrs.get(field_name)

            if not field_value_attr:
                attrs[field_name] = None  # To replace empty "" string value with None valid for FloatField
            else:
                validated_field_value = get_abs_float_from_str_or_number(field_value_attr)

                if not validated_field_value:
                    error_messages.append(
                        NOT_POSITIVE_FLOAT_OR_INT(field_name,
                                                  field_value_attr))
                    # raise serializers.ValidationError(gettext_lazy(
                    #     NOT_POSITIVE_FLOAT_OR_INT(field_name,
                    #                               field_value_attr)))
                else:
                    attrs[field_name] = validated_field_value  # Replacing by the value converted to the valid formant

        if GroupClientProgress.objects.filter(
                group_many_client=group_many_client_attr,
                check_point_date=check_point_date_attr).exists():
            error_messages.append(GROUP_CLIENT_DATE_EXISTS)
            # raise serializers.ValidationError(
            #     gettext_lazy(GROUP_CLIENT_DATE_EXISTS))

        if error_messages:
            error_messages_str = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(error_messages_str))

        return attrs



class GroupClientProgressRetrieveUpdateDeleteModelSerializer(serializers.ModelSerializer):
    group_many_client = serializers.SlugRelatedField(
                                slug_field="id",
                                read_only=False,
                                queryset=GroupManyClient.objects.all())

    self_satisfaction_level = serializers.SlugRelatedField(
                                slug_field="id",
                                read_only=False,
                                queryset=SelfSatisfactionLevel.objects.all())

    emotional_level = serializers.SlugRelatedField(
                                slug_field="id",
                                read_only=False,
                                queryset=EmotionalLevel.objects.all())

    task_completed = serializers.BooleanField(read_only=False,
                                              initial=False)

    creator = serializers.SlugRelatedField(
                                        slug_field="id",
                                        read_only=False,
                                        queryset=User.objects.all())

    current_weight = serializers.CharField(
        max_length=10,
        allow_blank=True, allow_null=True,
        help_text=gettext_lazy(ENTER_POSITIVE_FLOAT_OR_INT_NUMBER))

    current_breast = serializers.CharField(
        max_length=10,
        allow_blank=True, allow_null=True,
        help_text=gettext_lazy(ENTER_POSITIVE_FLOAT_OR_INT_NUMBER))

    current_shoulders = serializers.CharField(
        max_length=10,
        allow_blank=True, allow_null=True,
        help_text=gettext_lazy(ENTER_POSITIVE_FLOAT_OR_INT_NUMBER))

    current_waist = serializers.CharField(
        max_length=10,
        allow_blank=True, allow_null=True,
        help_text=gettext_lazy(ENTER_POSITIVE_FLOAT_OR_INT_NUMBER))

    current_hips = serializers.CharField(
        max_length=10,
        allow_blank=True, allow_null=True,
        help_text=gettext_lazy(ENTER_POSITIVE_FLOAT_OR_INT_NUMBER))

    current_height = serializers.CharField(
        max_length=10,
        allow_blank=True, allow_null=True,
        help_text=gettext_lazy(ENTER_POSITIVE_FLOAT_OR_INT_NUMBER))

    class Meta:
        model = GroupClientProgress
        # fields = "__all__"
        fields = ["id",
                  "group_many_client",
                  "self_satisfaction_level",
                  "emotional_level",
                  "task_completed",
                  "check_point_date",
                  "current_weight",
                  "current_breast",
                  "current_shoulders",
                  "current_waist",
                  "current_hips",
                  "current_height",
                  "description",
                  "note",
                  "created_at",
                  "updated_at",
                  "creator",
                  ]

    def get_fields(self):
        fields = super().get_fields()

        fields["group_many_client"].queryset = GroupManyClient.objects.order_by(
            "training_group_id__training_group_code", # order by field, defined pk field and curr field
            "training_group_id__training_group_name", # order by field, defined pk field and curr field
            "client_id__user")                        # order by __str__, defined only pk field without curr field

        fields["self_satisfaction_level"].queryset = SelfSatisfactionLevel.objects.order_by(
            "-value", "name")

        fields["emotional_level"].queryset = EmotionalLevel.objects.order_by(
            "-value", "name")

        try:
            current_user_id = self.context["request"].user.id
            fields["creator"].queryset = User.objects.filter(id=current_user_id)
            return fields
        except (ValueError, Exception) as error:
            print(gettext_lazy(EXCEPTION_INFO(error)))
        return fields


    def to_representation(self, instance):  # Forms dictionary with response fields (fields-keys can be added)
        representation = super().to_representation(instance)
        representation["group_many_client"] = str(instance.group_many_client)
        representation["self_satisfaction_level"] = str(instance.self_satisfaction_level)
        representation["emotional_level"] = str(instance.emotional_level)
        representation["creator"] = str(instance.creator)

        representation["training_group_id"] = instance.group_many_client.training_group_id.id                    # Field
        representation["training_group_code"] = instance.group_many_client.training_group_id.training_group_code # Field
        representation["training_group_name"] = instance.group_many_client.training_group_id.training_group_name # Field
        representation["training_group_full_name"] = instance.group_many_client.training_group_id.full_name  # @Property
        representation["training_group_str"] = str(instance.group_many_client.training_group_id)             # __str__

        representation["client_id"] = instance.group_many_client.client_id.id
        representation["client_full_name"] = instance.group_many_client.client_id.full_name
        representation["client_str"] = str(instance.group_many_client.client_id)

        representation["self_satisfaction_level_id"] = instance.self_satisfaction_level.id
        representation["self_satisfaction_level_value"] = instance.self_satisfaction_level.value
        representation["self_satisfaction_level_name"] = instance.self_satisfaction_level.name
        representation["self_satisfaction_level_full_name"] = instance.self_satisfaction_level.full_name

        representation["emotional_level_id"] = instance.emotional_level.id
        representation["emotional_level_value"] = instance.emotional_level.value
        representation["emotional_level_name"] = instance.emotional_level.name
        representation["emotional_level_full_name"] = instance.emotional_level.full_name

        representation["creator_id"] = str(instance.creator.id)

        return representation

    def validate(self, attrs):
        attrs = super().validate(attrs)

        error_messages = []

        group_many_client_attr = attrs.get("group_many_client")
        if not group_many_client_attr:
            error_messages.append(GROUP_CLIENT_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(GROUP_CLIENT_REQUIRED))

        self_satisfaction_level_attr = attrs.get("self_satisfaction_level")
        if not self_satisfaction_level_attr:
            error_messages.append(SELF_SATISFACTION_LEVEL_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(SELF_SATISFACTION_LEVEL_REQUIRED))

        emotional_level_attr = attrs.get("emotional_level")
        if not emotional_level_attr:
            error_messages.append(EMOTIONAL_LEVEL_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(EMOTIONAL_LEVEL_REQUIRED))

        check_point_date_attr = attrs.get("check_point_date")
        if not check_point_date_attr:
            error_messages.append(CHECK_POINT_DATE_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CHECK_POINT_DATE_REQUIRED))

        creator_attr = attrs.get("creator")
        if not creator_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))


        float_fields_to_validate_names = ["current_weight",
                                          "current_breast",
                                          "current_shoulders",
                                          "current_waist",
                                          "current_hips",
                                          "current_height"]

        for field_name in float_fields_to_validate_names:
            field_value_attr = attrs.get(field_name)

            if not field_value_attr:
                attrs[field_name] = None  # To replace empty "" string value with None valid for FloatField
            else:
                validated_field_value = get_abs_float_from_str_or_number(field_value_attr)

                if not validated_field_value:
                    error_messages.append(
                        NOT_POSITIVE_FLOAT_OR_INT(field_name,
                                                  field_value_attr))
                    # raise serializers.ValidationError(gettext_lazy(
                    #     NOT_POSITIVE_FLOAT_OR_INT(field_name,
                    #                               field_value_attr)))
                else:
                    attrs[field_name] = validated_field_value  # Replacing by the value converted to the valid formant


        client_progress_id_view_passed_req_param = (
                                self.context.get("client_progress_id"))

        old_group_many_client = GroupClientProgress.objects.get(
            id=client_progress_id_view_passed_req_param).group_many_client
        old_check_point_date = GroupClientProgress.objects.get(
            id=client_progress_id_view_passed_req_param).check_point_date

        new_check_point_date = attrs.get("check_point_date")
        new_group_many_client = attrs.get("group_many_client")

        if (new_group_many_client != old_group_many_client
                and new_check_point_date != old_check_point_date):
            if GroupClientProgress.objects.filter(
                    group_many_client=group_many_client_attr,
                    check_point_date=check_point_date_attr).exists():
                error_messages.append(GROUP_CLIENT_DATE_EXISTS)
                # raise serializers.ValidationError(
                #     gettext_lazy(GROUP_CLIENT_DATE_EXISTS))

        if error_messages:
            error_messages_str = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(error_messages_str))

        attrs.setdefault("task_completed", False)  # If None, should be False, fixed django bug Boolean field None value

        return attrs
