from rest_framework import serializers, request
from rest_framework.validators import UniqueValidator

from django.utils.translation import gettext_lazy

from django.db.models import Q

from apps.api.messages_api.messages_non_front import EXCEPTION_INFO

from apps.api.messages_api.messages_errors import (
    DEPARTMENT_NAME_REQUIRED,
    DEPARTMENT_NAME_ALREADY_EXISTS,
    COMPANY_NAME_REQUIRED,
    ADMINISTRATOR_REQUIRED,
    CREATOR_REQUIRED,
)

from apps.api.department.models import Department
from apps.api.user.models import User
from apps.api.company.models import Company
from apps.api.administrator.models import Administrator

from apps.api.user.serializers import UsersAllFieldsNoPermissionsSerializer



class DepartmentAllFieldsModelSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()

    administrator = serializers.SerializerMethodField()

    creator = serializers.SlugRelatedField(slug_field="full_name",
                                           read_only=True)

    class Meta:
        model = Department
        # fields = "__all__"
        fields = ["id",
                  "name",
                  "is_active",
                  "address",
                  "description",
                  "note",
                  "created_at",
                  "updated_at",
                  "company",
                  "administrator",
                  "creator",
                  ]

    def get_company(self, obj):
        company = {"company_id": obj.company.id,
                   "company_name": obj.company.name,
                   "company_is_active": obj.company.is_active}
        return company

    def get_administrator(self, obj):
        administrator = {
            "administrator_id": obj.administrator.id,
            "administrator_first_name": obj.administrator.first_name,
            "administrator_last_name": obj.administrator.last_name,
            "administrator_phone": obj.administrator.phone,
            "administrator_user": obj.administrator.user.full_name,
            "administrator_user_is_active": obj.administrator.user.is_active}
        return administrator



class DepartmentCreateModelSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(slug_field="name",
                                           read_only=False,
                                           queryset=Company.objects.all())

    administrator = serializers.SlugRelatedField(
                                slug_field="id",
                                read_only=False,
                                queryset=Administrator.objects.all())

    creator = serializers.SlugRelatedField(slug_field="id",
                                           read_only=False,
                                           queryset=User.objects.all())

    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Department
        # fields = "__all__"
        fields = ["id",
                  "name",
                  "is_active",
                  "company",
                  "administrator",
                  "address",
                  "description",
                  "note",
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
        representation["administrator_user_full_name"] = instance.administrator.user.full_name
        representation["creator_user_full_name"] = instance.creator.full_name
        return representation


    def validate(self, attrs):
        attrs = super().validate(attrs)

        name_attr = attrs.get("name")
        company_attr = attrs.get("company")
        administrator_attr = attrs.get("administrator")
        creator_attr = attrs.get("creator")


        error_messages = []

        if not name_attr:
            error_messages.append(DEPARTMENT_NAME_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(DEPARTMENT_NAME_REQUIRED))

        if not company_attr:
            error_messages.append(COMPANY_NAME_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(COMPANY_NAME_REQUIRED))

        if not administrator_attr:
            error_messages.append(ADMINISTRATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(ADMINISTRATOR_REQUIRED))

        if not creator_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))

        if Department.objects.filter(name=name_attr).exists():
            error_messages.append(DEPARTMENT_NAME_ALREADY_EXISTS)
            # raise serializers.ValidationError(
            #     gettext_lazy(DEPARTMENT_NAME_ALREADY_EXISTS))

        if error_messages:
            ERROR_MESSAGES_STR = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(ERROR_MESSAGES_STR))

        return attrs



class DepartmentRetrieveUpdateDeleteModelSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(slug_field="name",
                                           read_only=False,
                                           queryset=Company.objects.all())

    administrator = serializers.SlugRelatedField(
                                slug_field="id",
                                read_only=False,
                                queryset=Administrator.objects.all())

    creator = serializers.SlugRelatedField(slug_field="id",
                                           read_only=False,
                                           queryset=User.objects.all())

    is_active = serializers.BooleanField(allow_null=False,
                                         initial=True)

    class Meta:
        model = Department
        # fields = "__all__"
        fields = ["id",
                  "name",
                  "is_active",
                  "company",
                  "administrator",
                  "address",
                  "description",
                  "note",
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
        representation["administrator_user_full_name"] = instance.administrator.user.full_name
        representation["creator_user_full_name"] = instance.creator.full_name
        return representation


    def validate(self, attrs):
        attrs = super().validate(attrs)

        name_attr = attrs.get("name")
        company_attr = attrs.get("company")
        administrator_attr = attrs.get("administrator")
        creator_attr = attrs.get("creator")


        error_messages = []

        if not name_attr:
            error_messages.append(DEPARTMENT_NAME_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(DEPARTMENT_NAME_REQUIRED))

        if not company_attr:
            error_messages.append(COMPANY_NAME_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(COMPANY_NAME_REQUIRED))

        if not administrator_attr:
            error_messages.append(ADMINISTRATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(ADMINISTRATOR_REQUIRED))

        if not creator_attr:
            error_messages.append(CREATOR_REQUIRED)
            # raise serializers.ValidationError(
            #     gettext_lazy(CREATOR_REQUIRED))

        department_id_from_view_passed_request_param = (
                                    self.context.get("department_id"))

        old_department_name = Department.objects.get(
                id=department_id_from_view_passed_request_param).name

        new_department_name = attrs.get("name")

        if new_department_name != old_department_name:
            if Department.objects.filter(name=new_department_name):
                error_messages.append(DEPARTMENT_NAME_ALREADY_EXISTS)
                # raise serializers.ValidationError(
                #     gettext_lazy(DEPARTMENT_NAME_ALREADY_EXISTS))

        if error_messages:
            ERROR_MESSAGES_STR = ", ".join(error_messages)
            raise serializers.ValidationError(
                gettext_lazy(ERROR_MESSAGES_STR))

        attrs.setdefault("is_active", False)  # If None, should be False, fixed django bug Boolean field None value

        return attrs
