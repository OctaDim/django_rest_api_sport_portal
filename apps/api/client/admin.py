from django.contrib import admin
# Register your models here.

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import CLIENT_CREATOR_IS_CURRENT_USER

from apps.api.messages_api.messages_fields import (USER,
                                                   USER_ID,
                                                   EMAIL,
                                                   USERNAME,
                                                   NICKNAME,
                                                   FIRST_NAME,
                                                   LAST_NAME,
                                                   PHONE,
                                                   IS_STAFF,
                                                   IS_SUPERUSER,
                                                   IS_TRAINER,
                                                   IS_VERIFIED,
                                                   IS_ACTIVE,
                                                   DATE_JOINED,
                                                   LAST_LOGIN,
                                                   )

from apps.api.client.models import Client
from apps.api.user.models import User
from apps.api.gender.models import Gender
from apps.api.client_status.models import ClientStatus
from apps.api.country.models import Country

from django.contrib import messages

from django.db.models import Q



@admin.register(Client)  # Option 1
class ClientAdmin(admin.ModelAdmin):
    # Defining fields and order to edit in the form and save
    # Possible to use all fields from the model by names defined in the model
    # <relative_table>__<field_name> does not work
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

    # Table displaying fields. Defining order and ordering
    # Possible to use all fields by names from the model without ordering
    # To order model fields or relative fields methods+decorator @admin.display() is necessary
    # Direct access (as "country") to the relative fields is allowed ()
    # <relative_table>__<field_name> does not work
    list_display = ["id",
                    # "user",  # If necessary
                    "get_user_email_and_order",
                    "get_user_username_and_order",
                    "get_user_nickname_and_order",
                    "get_user_id_and_order",
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
                    "get_user_is_staff_and_order",
                    "get_user_is_superuser_and_order",
                    "get_user_is_trainer_and_order",
                    "get_user_is_verified_and_order",
                    "get_user_is_active_and_order",
                    "get_user_date_joined_and_order",
                    "get_user_last_login_and_order",
                    "created_at",
                    "updated_at",
                    "client_creator",
                    ]

    # All search fields defined as <relative_table>__<field_name> only
    # Impossible to use relative FK fields __str__
    # Direct access (as "country") to the relative fields is not allowed ()
    search_fields = ["id",
                     "user__email",
                     "user__username",
                     "user__nickname",
                     "user__id",
                     "thumbnail_link",
                     "client_status__id",
                     "client_status__name",
                     "first_name",
                     "last_name",
                     "phone",
                     "country__id",
                     "country__name",
                     "address",
                     "gender__id",
                     "gender__name",
                     "birth_date",
                     "bibliography",
                     "note",
                     "user__is_staff",
                     "user__is_superuser",
                     "user__is_trainer",
                     "user__is_verified",
                     "user__is_active",
                     "user__date_joined",
                     "user__last_login",
                     "created_at",
                     "updated_at",
                     "client_creator__id",
                     ]

    # All search fields defined as <relative_table>__<field_name> only
    # Possible to use relative FK fields __str__
    # Direct access (as "country") to the relative fields is allowed ()
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
        return obj.user
        # return obj.user.objects.filter(is_staff=False, is_superuser=False, is_trainer=False)

    @admin.display(ordering="user__id",  # Relative model field
                   description=gettext_lazy(USER_ID))
    def get_user_id_and_order(self, obj):
        return obj.user.id


    @admin.display(ordering="user__email",  # Relative model field
                   description=gettext_lazy(EMAIL))
    def get_user_email_and_order(self, obj):
        return obj.user.email


    @admin.display(ordering="user__username",  # Relative model field
                   description=gettext_lazy(USERNAME))
    def get_user_username_and_order(self, obj):
        return obj.user.username
    #
    #
    @admin.display(ordering="user__nickname",  # Relative model field
                   description=gettext_lazy(NICKNAME))
    def get_user_nickname_and_order(self, obj):
        return obj.user.nickname


    # @admin.display(ordering="first_name",  # Self model field
    #                description=gettext_lazy(FIRST_NAME))
    # def get_administrator_first_name_ordered(self, obj):
    #     return obj.first_name


    # @admin.display(ordering="last_name",  # Self model field
    #                description=gettext_lazy(LAST_NAME))
    # def get_administrator_last_name_ordered(self, obj):
    #     return obj.last_name


    # @admin.display(ordering="phone",  # Self model field
    #                description=gettext_lazy(PHONE))
    # def get_administrator_phone_ordered(self, obj):
    #     return obj.phone


    @admin.display(boolean=True,  # Boolean, relative model field
                   ordering="user__is_staff",
                   description=gettext_lazy(IS_STAFF))
    def get_user_is_staff_and_order(self, obj):
        return obj.user.is_staff


    @admin.display(boolean=True,  # Boolean, relative model field
                   ordering="user__is_superuser",
                   description=gettext_lazy(IS_SUPERUSER))
    def get_user_is_superuser_and_order(self, obj):
        return obj.user.is_superuser


    @admin.display(boolean=True,  # Boolean, relative model field
                   ordering="user__is_trainer",
                   description=gettext_lazy(IS_TRAINER))
    def get_user_is_trainer_and_order(self, obj):
        return obj.user.is_trainer


    @admin.display(boolean=True,  # Boolean, relative model field
                   ordering="user__is_verified",
                   description=gettext_lazy(IS_VERIFIED))
    def get_user_is_verified_and_order(self, obj):
        return obj.user.is_verified


    @admin.display(boolean=True,  # Boolean, relative model field
                   ordering="user__is_active",
                   description=gettext_lazy(IS_ACTIVE))
    def get_user_is_active_and_order(self, obj):
        return obj.user.is_active


    @admin.display(ordering="date_joined",  # Date, relative model field
                   description=gettext_lazy(DATE_JOINED))
    def get_user_date_joined_and_order(self, obj):
        return obj.user.date_joined


    @admin.display(ordering="last_login",  # Date, relative model field
                   description=gettext_lazy(LAST_LOGIN))
    def get_user_last_login_and_order(self, obj):
        return obj.user.last_login
