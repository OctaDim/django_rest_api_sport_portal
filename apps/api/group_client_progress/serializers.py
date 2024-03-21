from rest_framework import serializers, request
from rest_framework.validators import UniqueValidator

from django.utils.translation import gettext_lazy

from django.db.models import Q

from apps.api.messages_api.messages_non_front import EXCEPTION_INFO

from apps.api.messages_api.messages_errors import (
    USER_REQUIRED,
    CLIENT_CREATOR_REQUIRED,
    CLIENT_WITH_USER_ALREADY_EXISTS,
                                    )

from apps.api.group_client_progress.models import GroupClientProgress
from apps.api.user.models import User

from apps.api.group_many_client.serializers import GroupManyClientModelSerializer

from apps.api.user.serializers import UsersAllFieldsNoPermissionsSerializer

from apps.api.client.validators import validate_image_size



class GroupClientProgressAllFieldsModelSerializer(serializers.ModelSerializer):
    # groups_many_clients = serializers.SerializerMethodField

    # group_client_id = GroupManyClientModelSerializer()
    #
    # group_client_id = serializers.SlugRelatedField(slug_field="id",
    #                                                read_only=True)
    #
    # self_satisfaction_level = serializers.SlugRelatedField(slug_field="name",
    #                                                read_only=True)
    #
    # emotional_level = serializers.SlugRelatedField(slug_field="name",
    #                                                read_only=True)
    #
    # creator = serializers.SlugRelatedField(slug_field="full_name",
    #                                              read_only=True)

    class Meta:
        model = GroupClientProgress
        fields = "__all__"
        # fields = ["id",
        #           "group_client_id",
        #           "group_client_id",
        #           "self_satisfaction_level",
        #           "emotional_level",
        #           "task_completed",
        #           "check_point_date",
        #           "current_weight",
        #           "current_breast",
        #           "current_shoulders",
        #           "current_waist",
        #           "current_hips",
        #           "current_height",
        #           "description",
        #           "note",
        #           "created_at",
        #           "updated_at",
        #           "creator",
        #           ]

        # def get_groups_many_clients(self, obj):
        #     groups_many_clients = {"group_id": obj..id}
        #     return {}


# class ClientCreateModelSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField(
#         slug_field="id",
#         read_only=False,
#         # validators=[UniqueValidator(queryset=User.objects.all())],  # Defined validation in validate() method
#         queryset=User.objects.filter(
#             Q(is_staff=False) & Q(is_superuser=False) & Q(is_trainer=False)
#         )
#     )
#
#     client_status = serializers.SlugRelatedField(
#                                     slug_field="name",
#                                     read_only=False,
#                                     queryset=ClientStatus.objects.all())
#
#     country = serializers.SlugRelatedField(slug_field="name",
#                                            read_only=False,
#                                            queryset=Country.objects.all())
#
#     gender = serializers.SlugRelatedField(slug_field="name",
#                                           read_only=False,
#                                           queryset=Gender.objects.all())
#
#     class Meta:
#         model = Client
#         unique_together = ("id", "user")
#         # fields = "__all__"  # Not used, if exclude is used (exclude= all-exclude)
#         fields = ["id",
#                   "user",
#                   "thumbnail_link",
#                   "first_name",
#                   "last_name",
#                   "phone",
#                   "address",
#                   "birth_date",
#                   "bibliography",
#                   "note",
#                   "created_at",
#                   "updated_at",
#                   "client_status",
#                   "country",
#                   "gender",
#                   "client_creator",
#                   ]
#
#
#     def to_representation(self, instance):  # Forms dictionary with response fields (fields-keys can be added)
#         representation = super().to_representation(instance)
#         representation["client_creator_full_name"] = instance.client_creator.full_name
#         representation["user_full_name"] = instance.user.full_name
#         representation["user_is_active"] = instance.user.is_active
#         representation["user_is_verified"] = instance.user.is_verified
#         representation["user_is_staff"] = instance.user.is_staff
#         representation["user_is_trainer"] = instance.user.is_trainer
#         representation["user_is_superuser"] = instance.user.is_superuser
#
#         return representation
#
#
#     def get_fields(self):
#         fields = super().get_fields()
#
#         try:
#             current_user_id = self.context["request"].user.id
#             fields["client_creator"].queryset = User.objects.filter(id=current_user_id)
#             return fields
#         except (ValueError, Exception) as error:
#             print(gettext_lazy(EXCEPTION_INFO(error)))
#
#         return fields
#
#
#     # def validate_thumbnail_link(self, value):
#     #     # Model field defined validator intercepts value before validation in serializer
#     #     return value
#
#
#     def validate(self, attrs):
#         attrs = super().validate(attrs)
#
#         user_attr = attrs.get("user")
#         client_creator_attr = attrs.get("client_creator")
#
#         error_messages = []
#
#         if not user_attr:
#             error_messages.append(USER_REQUIRED)
#             # raise serializers.ValidationError(
#             #     gettext_lazy(USER_REQUIRED))
#
#         if not client_creator_attr:
#             error_messages.append(CLIENT_CREATOR_REQUIRED)
#             # raise serializers.ValidationError(
#             #     gettext_lazy(CLIENT_CREATOR_REQUIRED))
#
#         if Client.objects.filter(user=user_attr).exists():
#             error_messages.append(CLIENT_WITH_USER_ALREADY_EXISTS)
#             # raise serializers.ValidationError(
#             #     gettext_lazy(CLIENT_WITH_USER_ALREADY_EXISTS))
#
#         if error_messages:
#             ERROR_MESSAGES_STR = ", ".join(error_messages)
#             raise serializers.ValidationError(
#                 gettext_lazy(ERROR_MESSAGES_STR))
#
#         return attrs
#
#
#
# class ClientRetrieveUpdateDeleteModelSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField(
#         slug_field="id",
#         read_only=False,
#         # validators=[UniqueValidator(queryset=User.objects.all())],  # Defined validation in validate() method
#         queryset=User.objects.filter(
#             Q(is_staff=False) & Q(is_superuser=False) & Q(is_staff=False)))
#
#     user_is_active = serializers.BooleanField(write_only=True,  # IMPORTANT: write_only=True if no model field
#                                               allow_null=False,
#                                               initial=True,
#                                               )
#
#     client_status = serializers.SlugRelatedField(
#                                     slug_field="name",
#                                     read_only=False,
#                                     queryset=ClientStatus.objects.all())
#
#     country = serializers.SlugRelatedField(slug_field="name",
#                                            read_only=False,
#                                            queryset=Country.objects.all())
#
#     gender = serializers.SlugRelatedField(slug_field="name",
#                                           read_only=False,
#                                           queryset=Gender.objects.all())
#
#     class Meta:
#         model = Client
#         unique_together = ("id", "user")
#         # fields = "__all__"  # Not used, if exclude is used (exclude= all-exclude)
#         fields = ["id",
#                   "user",
#                   "user_is_active",
#                   "thumbnail_link",
#                   "first_name",
#                   "last_name",
#                   "phone",
#                   "address",
#                   "birth_date",
#                   "bibliography",
#                   "note",
#                   "created_at",
#                   "updated_at",
#                   "client_status",
#                   "country",
#                   "gender",
#                   "client_creator",
#                   ]
#
#     def to_representation(self, instance):  # Forms dictionary with response fields (fields-keys can be added)
#         representation = super().to_representation(instance)
#         representation["client_creator_full_name"] = instance.client_creator.full_name
#         representation["user_full_name"] = instance.user.full_name
#         representation["user_is_active"] = instance.user.is_active
#         representation["user_is_verified"] = instance.user.is_verified
#         representation["user_is_staff"] = instance.user.is_staff
#         representation["user_is_trainer"] = instance.user.is_trainer
#         representation["user_is_superuser"] = instance.user.is_superuser
#         return representation
#
#
#     def get_fields(self):
#         fields = super().get_fields()
#
#         try:
#             current_user_id = self.context['request'].user.id
#             fields["client_creator"].queryset = User.objects.filter(id=current_user_id)
#             return fields
#         except (ValueError, Exception) as error:
#             print(gettext_lazy(EXCEPTION_INFO(error)))
#
#         return fields
#
#
#     # def validate_thumbnail_link(self, value):
#     #     # Model field defined validator intercepts value before validation in serializer
#     #     return value
#
#
#     def validate(self, attrs, *args, **kwargs):
#         attrs = super().validate(attrs)
#
#         error_messages = []
#
#         user_in_attrs = attrs.get("user")
#         client_creator_in_attrs = attrs.get("client_creator")
#
#         if not user_in_attrs:
#             error_messages.append(USER_REQUIRED)
#             # raise serializers.ValidationError(
#             #     gettext_lazy(USER_REQUIRED))
#
#         if not client_creator_in_attrs:
#             error_messages.append(CLIENT_CREATOR_REQUIRED)
#             # raise serializers.ValidationError(
#             #     gettext_lazy(CLIENT_CREATOR_REQUIRED))
#
#         client_id_from_view_passed_request_param = self.context.get("client_id")
#         old_user_id_in_client = Client.objects.get(
#                         id=client_id_from_view_passed_request_param).user.id
#         new_user_id_in_client = attrs.get("user").id
#         user_in_attrs = attrs.get("user")
#
#         if new_user_id_in_client != old_user_id_in_client:
#             if Client.objects.filter(user=user_in_attrs):
#                 error_messages.append(CLIENT_WITH_USER_ALREADY_EXISTS)
#                 # raise serializers.ValidationError(
#                 #     gettext_lazy(CLIENT_WITH_USER_ALREADY_EXISTS))
#
#         if error_messages:
#             error_messages_str = ", ".join(error_messages)
#             raise serializers.ValidationError(
#                 gettext_lazy(error_messages_str))
#
#         attrs.setdefault("user_is_active", False)  # If None, should be False, fixed django bug Boolean field None value
#
#         return attrs
