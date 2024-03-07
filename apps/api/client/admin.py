from django.contrib import admin
# Register your models here.

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import CLIENT_CREATOR_IS_CURRENT_USER

from apps.api.messages_api.messages_fields import (CLIENT,
                                                   USER,
                                                   USER_ID,
                                                   EMAIL,
                                                   USERNAME,
                                                   NICKNAME,
                                                   FIRST_NAME,
                                                   LAST_NAME,
                                                   PHONE,
                                                   IS_STAFF,
                                                   IS_VERIFIED,
                                                   IS_ACTIVE,
                                                   DATE_JOINED,
                                                   LAST_LOGIN,
                                                   CREATED_AT,
                                                   UPDATED_AT,
                                                   CLIENT_CREATOR, IS_TRAINER, IS_SUPERUSER)

from apps.api.client.models import Client
from apps.api.user.models import User
from apps.api.gender.models import Gender
from apps.api.client_status.models import ClientStatus
from apps.api.country.models import Country

from django.contrib import messages

from django.db.models import Q



@admin.register(Client)  # Option 1
class ClientAdmin(admin.ModelAdmin):
    fields = ["user",  # Form fields and order
              "thumbnail_link",
              "client_status",
              "first_name",
              "last_name",
              "phone",
              "country",
              "address",
              "gender",
              "birth_date",
              "bibliography",
              "note",
              "client_creator",
              ]

    list_display = ["id",  # Table fields and order
                    "get_user_email",
                    "get_user_username",
                    "get_user_nickname",
                    "get_user_id",
                    "thumbnail_link",
                    "client_status",
                    # "get_user_first_name",
                    # "get_user_last_name",
                    # "get_user_phone",
                    "first_name",
                    "last_name",
                    "phone",
                    "country",
                    "address",
                    "gender",
                    "birth_date",
                    "bibliography",
                    "note",
                    "get_user_is_staff",
                    "get_user_is_superuser",
                    "get_user_is_trainer",
                    "get_user_is_verified",
                    "get_user_is_active",
                    "get_user_date_joined",
                    "get_user_last_login",
                    "created_at",
                    "updated_at",
                    "client_creator",
                    ]

    search_fields = ["id",
                    "get_user_email",
                    "get_user_username",
                    "get_user_nickname",
                    "get_user_id",
                    "thumbnail_link",
                    "client_status",
                    # "get_user_first_name",
                    # "get_user_last_name",
                    # "get_user_phone",
                    "first_name",
                    "last_name",
                    "phone",
                    "country",
                    "address",
                    "gender",
                    "birth_date",
                    "bibliography",
                    "note",
                    "get_user_is_staff",
                    "get_user_is_superuser",
                    "get_user_is_trainer",
                    "get_user_is_verified",
                    "get_user_is_active",
                    "get_user_date_joined",
                    "get_user_last_login",
                    "created_at",
                    "updated_at",
                    "client_creator",
                    ]

    list_filter = ["client_status",
                   "country",
                   "gender",
                   "birth_date",
                   "user__is_staff",
                   "user__is_superuser",
                   "user__is_trainer",
                   "user__is_verified",
                   "user__is_active",
                   "user__date_joined",
                   "user__last_login",
                   "created_at",
                   "updated_at",
                   "client_creator",
                   ]

    def get_queryset(self, request):  # Getting queryset once, not each time getting related field, faster
        query_set = super().get_queryset(request)
        # query_set = super().get_queryset(
        #     request).select_related("user").filter(
        #     user__is_staff=False, user__is_superuser=False, user__is_trainer=False)
        # # query_set = super().get_queryset(request).select_related('user')  # To display all users
        # # query_set = super(AdministratorAdmin, self).get_queryset(request).select_related('user')  # To display all users

        return query_set

    def formfield_for_foreignkey(self, db_field, request, **kwargs):  # Values available to choice
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(
                is_staff=False, is_superuser=False, is_trainer=False)

        if (db_field.name == "client_creator"
                and request.user.is_authenticated):
                    kwargs["queryset"] = User.objects.filter(pk=request.user.pk)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def save_model(self, request, obj, form, change):  # Default value for new object
        obj.client_creator = User.objects.get(id=request.user.id)  # Creator must always be current user
        messages.info(request=request,
                      message=gettext_lazy(CLIENT_CREATOR_IS_CURRENT_USER))
        super().save_model(request, obj, form, change)


    @admin.display(ordering="user",
                   description=gettext_lazy(USER))  # User __str__
    def get_user(self, obj):
        return obj.user.objects.filter(is_staff=False, is_superuser=False, is_trainer=False)


    @admin.display(ordering="user__id",
                   description=gettext_lazy(USER_ID))
    def get_user_id(self, obj):
        return obj.user.id


    @admin.display(ordering="email",
                   description=gettext_lazy(EMAIL))
    def get_user_email(self, obj):
        return obj.user.email


    @admin.display(ordering="username",
                   description=gettext_lazy(USERNAME))
    def get_user_username(self, obj):
        return obj.user.username


    @admin.display(ordering="nickname",
                   description=gettext_lazy(NICKNAME))
    def get_user_nickname(self, obj):
        return obj.user.nickname


    # @admin.display(description=gettext_lazy(FIRST_NAME))
    # def get_user_first_name(self, obj):
    #     return obj.user.first_name


    # @admin.display(description=gettext_lazy(LAST_NAME))
    # def get_user_last_name(self, obj):
    #     return obj.user.last_name


    # @admin.display(description=gettext_lazy(PHONE))
    # def get_user_phone(self, obj):
    #     return obj.user.phone


    @admin.display(boolean=True,
                   ordering="user__is_staff",
                   description=gettext_lazy(IS_STAFF))
    def get_user_is_staff(self, obj):
        return obj.user.is_staff

    @admin.display(boolean=True,
                   ordering="user__is_trainer",
                   description=gettext_lazy(IS_TRAINER))
    def get_user_is_trainer(self, obj):
        return obj.user.is_trainer

    @admin.display(boolean=True,
                   ordering="user__is_superuser",
                   description=gettext_lazy(IS_SUPERUSER))
    def get_user_is_superuser(self, obj):
        return obj.user.is_superuser


    @admin.display(boolean=True,
                   ordering="user__is_verified",
                   description=gettext_lazy(IS_VERIFIED))
    def get_user_is_verified(self, obj):
        return obj.user.is_verified


    @admin.display(boolean=True,
                   ordering="user__is_active",
                   description=gettext_lazy(IS_ACTIVE))
    def get_user_is_active(self, obj):
        return obj.user.is_active


    @admin.display(ordering="date_joined",
                   description=gettext_lazy(DATE_JOINED))
    def get_user_date_joined(self, obj):
        return obj.user.date_joined


    @admin.display(ordering="last_login",
                   description=gettext_lazy(LAST_LOGIN))
    def get_user_last_login(self, obj):
        return obj.user.last_login


    @admin.display(ordering="created_at",
                   description=gettext_lazy(CREATED_AT))
    def get_user_created_at(self, obj):
        return obj.user.created_at


    @admin.display(ordering="updated_at",
                   description=gettext_lazy(UPDATED_AT))
    def get_user_updated_at(self, obj):
        return obj.user.updated_at

    @admin.display(ordering="client_creator",
                   description=gettext_lazy(CLIENT_CREATOR))
    def client_creator(self, obj):
        return obj.client_creator
