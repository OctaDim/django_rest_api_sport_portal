from rest_framework import serializers, request
from rest_framework.validators import UniqueValidator

from django.utils.translation import gettext_lazy

from django.db.models import Q

from apps.api.messages_api.messages_non_front import EXCEPTION_INFO

from apps.api.messages_api.messages_errors import (
                                        DEPARTMENT_REQUIRED,
                                        TRAINING_GROUP_CODE_REQUIRED,
                                        TRAINING_YEAR_REQUIRED,
                                        START_DATE_REQUIRED,
                                        FINISH_DATE_REQUIRED,
                                        CREATOR_REQUIRED,
                                        TRAINING_GROUP_CODE_ALREADY_EXISTS,
                                        )

from apps.api.training_group.models import TrainingGroup
from apps.api.training_year.models import TrainingYear
from apps.api.department.models import Department
from apps.api.client.models import Client
from apps.api.administrator.models import Administrator
from apps.api.coach.models import Coach
from apps.api.user.models import User

from apps.api.user.serializers import UsersAllFieldsNoPermissionsSerializer



class TrainingGroupAllFieldsModelSerializer(serializers.ModelSerializer):
    training_year = serializers.SlugRelatedField(slug_field="full_name",
                                                 read_only=True)

    department = serializers.SerializerMethodField()

    administrator = serializers.SlugRelatedField(slug_field="full_name",
                                                 many=True,
                                                 read_only=True)

    client = serializers.SlugRelatedField(slug_field="full_name",
                                          many=True,
                                          read_only=True)

    coach = serializers.SlugRelatedField(slug_field="full_name",
                                         many=True,
                                         read_only=True)

    creator = serializers.SlugRelatedField(slug_field="full_name",
                                           read_only=True)

    class Meta:
        model = TrainingGroup
        # fields = "__all__"
        fields = ["id",
                  "training_group_code",
                  "training_group_name",
                  "is_active",
                  "description",
                  "note",
                  "training_year",
                  "start_date",
                  "finish_date",
                  "department",
                  "administrator",
                  "client",
                  "coach",
                  "created_at",
                  "updated_at",
                  "creator",
                  ]

    def get_department(self, obj):
        department = {
            "department_str": str(obj.department),
            "department_id": obj.department.id,
            "department_name": obj.department.name,
            "department_company": obj.department.company.name,
            "department_administrator": str(obj.department.administrator),
            "department_full_name": obj.department.full_name}
        return department


class TrainingGroupCreateModelSerializer(serializers.ModelSerializer):
    training_year = serializers.SlugRelatedField(slug_field="name",
                                                 read_only=False,
                                                 queryset=TrainingYear.objects.all())

    department = serializers.SlugRelatedField(slug_field="name",
                                              read_only=False,
                                              queryset=Department.objects.all())

    administrator = serializers.SlugRelatedField(slug_field="id",
                                                 many=True,
                                                 read_only=False,
                                                 queryset=Administrator.objects.all())

    client = serializers.SlugRelatedField(slug_field="id",
                                          many=True,
                                          read_only=False,
                                          queryset = Client.objects.all())

    coach = serializers.SlugRelatedField(slug_field="id",
                                         many=True,
                                         read_only=False,
                                         queryset=Coach.objects.all())

    creator = serializers.SlugRelatedField(slug_field="id",
                                           read_only=False,
                                           queryset=User.objects.all())

    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = TrainingGroup
        # fields = "__all__"
        fields = ["id",
                  "training_group_code",
                  "training_group_name",
                  "is_active",
                  "description",
                  "note",
                  "training_year",
                  "start_date",
                  "finish_date",
                  "department",
                  "administrator",
                  "client",
                  "coach",
                  "created_at",
                  "updated_at",
                  "creator",
                  ]

    def get_fields(self):
        fields = super().get_fields()
        fields["training_year"].queryset = TrainingYear.objects.order_by("name")
        fields["department"].queryset = Department.objects.order_by("company", "name")
        fields["administrator"].queryset = Administrator.objects.order_by("user")
        fields["client"].queryset = Client.objects.order_by("user")
        fields["coach"].queryset = Coach.objects.order_by("user")

        try:
            current_user_id = self.context["request"].user.id
            fields["creator"].queryset = User.objects.filter(id=current_user_id)
            return fields
        except (ValueError, Exception) as error:
            print(gettext_lazy(EXCEPTION_INFO(error)))
        return fields

    def to_representation(self, instance):  # Forms dictionary with response fields (fields-keys can be added)
        representation = super().to_representation(instance)
        representation["training_year_full_name"] = instance.training_year.full_name
        representation["department_full_name"] = instance.department.full_name
        representation["creator_user_full_name"] = instance.creator.full_name
        return representation


    def validate(self, attrs):
        attrs = super().validate(attrs)

        error_messages = []

        training_group_code_attr = attrs.get("training_group_code")
        if not training_group_code_attr:
            error_messages.append(TRAINING_GROUP_CODE_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(TRAINING_GROUP_CODE_REQUIRED))

        training_year_attr = attrs.get("training_year")
        if not training_year_attr:
            error_messages.append(TRAINING_YEAR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(TRAINING_YEAR_REQUIRED))

        start_date_attr = attrs.get("start_date")
        if not start_date_attr:
            error_messages.append(START_DATE_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(START_DATE_REQUIRED))

        finish_date_attr = attrs.get("finish_date")
        if not finish_date_attr:
            error_messages.append(FINISH_DATE_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(FINISH_DATE_REQUIRED))

        department_attr = attrs.get("department")
        if not department_attr:
            error_messages.append(DEPARTMENT_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(DEPARTMENT_REQUIRED))

        creator_attr = attrs.get("creator")
        if not creator_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))

        creator_attr = attrs.get("creator")
        if not creator_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))


        if TrainingGroup.objects.filter(
                training_group_code=training_group_code_attr).exists():
            error_messages.append(TRAINING_GROUP_CODE_ALREADY_EXISTS)
            # raise serializers.ValidationError(
            #     gettext_lazy(TRAINING_GROUP_CODE_ALREADY_EXISTS))

        if error_messages:
            ERROR_MESSAGES_STR = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(ERROR_MESSAGES_STR))

        return attrs



class TrainingGroupRetrieveUpdateDeleteModelSerializer(serializers.ModelSerializer):
    training_year = serializers.SlugRelatedField(slug_field="name",
                                                 read_only=False,
                                                 queryset=TrainingYear.objects.all())

    department = serializers.SlugRelatedField(slug_field="name",
                                              read_only=False,
                                              queryset=Department.objects.all())

    administrator = serializers.SlugRelatedField(slug_field="id",
                                                 many=True,
                                                 read_only=False,
                                                 queryset=Administrator.objects.all())

    client = serializers.SlugRelatedField(slug_field="id",
                                          many=True,
                                          read_only=False,
                                          queryset = Client.objects.all())

    coach = serializers.SlugRelatedField(slug_field="id",
                                         many=True,
                                         read_only=False,
                                         queryset=Coach.objects.all())

    creator = serializers.SlugRelatedField(slug_field="id",
                                           read_only=False,
                                           queryset=User.objects.all())

    is_active = serializers.BooleanField(read_only=False,
                                         initial=True)

    class Meta:
        model = TrainingGroup
        # fields = "__all__"
        fields = ["id",
                  "training_group_code",
                  "training_group_name",
                  "is_active",
                  "description",
                  "note",
                  "training_year",
                  "start_date",
                  "finish_date",
                  "department",
                  "administrator",
                  "client",
                  "coach",
                  "created_at",
                  "updated_at",
                  "creator",
                  ]

    def get_fields(self):
        fields = super().get_fields()
        fields["training_year"].queryset = TrainingYear.objects.order_by("name")
        fields["department"].queryset = Department.objects.order_by("company", "name")
        fields["administrator"].queryset = Administrator.objects.order_by("user")
        fields["client"].queryset = Client.objects.order_by("user")
        fields["coach"].queryset = Coach.objects.order_by("user")

        try:
            current_user_id = self.context["request"].user.id
            fields["creator"].queryset = User.objects.filter(id=current_user_id)
            return fields
        except (ValueError, Exception) as error:
            print(gettext_lazy(EXCEPTION_INFO(error)))
        return fields

    def to_representation(self, instance):  # Forms dictionary with response fields (fields-keys can be added)
        representation = super().to_representation(instance)
        representation["training_year_full_name"] = instance.training_year.full_name
        representation["department_full_name"] = instance.department.full_name
        representation["creator_user_full_name"] = instance.creator.full_name
        return representation

    def validate(self, attrs):
        attrs = super().validate(attrs)

        error_messages = []

        training_group_code_attr = attrs.get("training_group_code")
        if not training_group_code_attr:
            error_messages.append(TRAINING_GROUP_CODE_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(TRAINING_GROUP_CODE_REQUIRED))

        training_year_attr = attrs.get("training_year")
        if not training_year_attr:
            error_messages.append(TRAINING_YEAR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(TRAINING_YEAR_REQUIRED))

        start_date_attr = attrs.get("start_date")
        if not start_date_attr:
            error_messages.append(START_DATE_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(START_DATE_REQUIRED))

        finish_date_attr = attrs.get("finish_date")
        if not finish_date_attr:
            error_messages.append(FINISH_DATE_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(FINISH_DATE_REQUIRED))

        department_attr = attrs.get("department")
        if not department_attr:
            error_messages.append(DEPARTMENT_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(DEPARTMENT_REQUIRED))

        creator_attr = attrs.get("creator")
        if not creator_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))

        creator_attr = attrs.get("creator")
        if not creator_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))

        training_group_id_view_passed_req_param = (
                                self.context.get("training_group_id"))

        old_training_group_code = TrainingGroup.objects.get(
            id=training_group_id_view_passed_req_param).training_group_code

        new_training_group_code = attrs.get("training_group_code")

        if new_training_group_code != old_training_group_code:
            if TrainingGroup.objects.filter(
                    training_group_code=new_training_group_code).exists():
                error_messages.append(TRAINING_GROUP_CODE_ALREADY_EXISTS)
                # raise serializers.ValidationError(
                #     gettext_lazy(TRAINING_GROUP_CODE_ALREADY_EXISTS))

        if error_messages:
            ERROR_MESSAGES_STR = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(ERROR_MESSAGES_STR))

        attrs.setdefault("is_active", False)  # If None, should be False, fixed django bug Boolean field None value

        return attrs
