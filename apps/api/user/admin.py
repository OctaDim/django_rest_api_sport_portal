from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# Register your models here.

# ##################################################################
# from django.contrib.auth.models import User  # Django default user
from apps.api.user.models import User  # Custom user
# ##################################################################

from django.utils.translation import gettext_lazy

from apps.api.messages_non_front import EXCEPTION_INFO

from apps.api.messages_errors import (PASSWORD_REQUIRED_MSG,
                                      PASSWORD2_REQUIRED_MSG,
                                      PASSWORDS_NOT_MATCH_ERROR)

from apps.api.messages_actions import (PASSWORD_SET_MSG,
                                       PASSWORD_UPDATED_MSG,
                                       USER_CREATOR_IS_CURRENT_USER,
                                       )

from apps.api.user.forms_admin_panel import UserCreationAdminCustomForm

from django import forms

from django.contrib import messages

from django.db.models import Q






@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    form = UserCreationAdminCustomForm
    # add_form = UserCreationAdminCustomForm

    exclude = ["date_joined"]

    fieldsets = []
    fields = ["password",
              "password2",
              "email", "username", "nickname",
              "first_name", "last_name", "phone",
              "is_staff", "is_trainer", "is_superuser",
              "is_verified", "is_active",
              "user_creator",
              "groups", "user_permissions",
              ]

    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    list_display = ["id", "email", "username", "nickname",
                    "is_staff", "is_trainer", "is_superuser",
                    "is_verified", "is_active",
                    "first_name", "last_name", "phone",
                    "date_joined",
                    "last_login", "updated_at",
                    "user_creator",
                    ]

    search_fields = ["id",
                    "email", "username", "nickname",
                    "first_name", "last_name", "phone",
                    "is_staff", "is_trainer", "is_superuser",
                    "is_verified", "is_active",
                    "date_joined",
                     "last_login", "updated_at",
                    "user_creator",
                    ]

    list_filter = ["is_staff", "is_trainer", "is_superuser",
                   "is_verified", "is_active",
                   "date_joined",
                   "last_login", "updated_at",
                   "user_creator"
                   ]


    def get_queryset(self, request):  # Getting queryset once, not each time getting related field, faster
        current_user_is_superuser = request.user.is_superuser
        current_user_is_staff = request.user.is_staff
        current_user_is_trainer = request.user.is_trainer

        if ((current_user_is_staff and not current_user_is_trainer)
                and not current_user_is_superuser):
            query_set = super().get_queryset(
                request).filter(is_superuser=False)
            # query_set = super().get_queryset(request)  # To display all users
            # query_set = super(AdministratorAdmin, self).get_queryset(request)  # To display all users
            return query_set

        if current_user_is_trainer:
            query_set = super().get_queryset(
                request).filter(is_superuser=False, is_staff=False)
            # query_set = super().get_queryset(request).  # To display all users
            # query_set = super(AdministratorAdmin, self).get_queryset(request).  # To display all users
            return query_set

        return super().get_queryset(request)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):  # Values available to choice
        if db_field.name == "user_creator":
            kwargs["queryset"] = User.objects.filter(pk=request.user.pk)  # Creator must always be current user

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        current_user_is_superuser = request.user.is_superuser
        current_user_is_staff= request.user.is_staff
        current_user_is_trainer= request.user.is_trainer

        try:
            if current_user_is_staff and not current_user_is_superuser:
                form.base_fields["is_superuser"].widget.attrs['disabled'] = 'disabled'
                form.base_fields["is_verified"].widget.attrs['disabled'] = 'disabled'

            if current_user_is_trainer:
                form.base_fields["is_staff"].widget.attrs['disabled'] = 'disabled'
                form.base_fields["is_trainer"].widget.attrs['disabled'] = 'disabled'
                form.base_fields["is_active"].widget.attrs['disabled'] = 'disabled'
                form.base_fields["user_creator"].widget.attrs['disabled'] = 'disabled'
                # form.base_fields["password"].widget.attrs['disabled'] = 'disabled'

        except (KeyError, Exception) as error:
            print(gettext_lazy(EXCEPTION_INFO(error)))

        return form

    def save_model(self, request, obj, form, change):
        form.is_valid()  # Validate and clean data via custom form

        ### SAVING USER CREATOR AS CURRENT USER ########################
        obj.user_creator = request.user  # Option 1
        # obj.user_creator = User.objects.get(id=request.user.id)  # Option 2
        messages.info(request=request,
                      message=gettext_lazy(USER_CREATOR_IS_CURRENT_USER))

        ### PASSWORD CREATING OR UPDATING, ENCRYPTING AND SAVING #######
        password = form.cleaned_data.get("password")

        if not change:  # Check. if the obj is new (created, but not changed)
            obj.set_password(password)  # Make and set hashed password, return None
            messages.info(request=request,
                          message=gettext_lazy(PASSWORD_SET_MSG))

        if change:  # Check. if the obj is updated (changed)
            obj.set_password(password)  # Make and set hashed password, return None
            messages.info(request=request,
                              message=gettext_lazy(PASSWORD_UPDATED_MSG))

        super().save_model(request, obj, form, change)



    ##################### FOR THE FUTURE ###############################
    ########## PASSWORD VALIDATING, IF NOT IN CUSTOM FORM ##############
    # password = form.cleaned_data.get("password")
    # password2 = form.cleaned_data.get("password2")
    #
    # error_messages = []
    # if not password:
    #     messages.error(request=request,
    #                    message=gettext_lazy(PASSWORD_REQUIRED_MSG))
    #     error_messages.append(PASSWORD_REQUIRED_MSG)
    #
    # if not password2:
    #     messages.error(request=request,
    #                    message=gettext_lazy(PASSWORD2_REQUIRED_MSG))
    #     error_messages.append(PASSWORD2_REQUIRED_MSG)
    #
    # if password != password2:
    #     forms.ValidationError("FORMS VALID ERROR")
    #     messages.error(request=request,
    #                    message=gettext_lazy(PASSWORDS_NOT_MATCH_ERROR))
    #     error_messages.append(PASSWORDS_NOT_MATCH_ERROR)
    #
    # if error_messages:
    #     error_messages_str = " // ".join(error_messages)
    #     raise exceptions.ValidationError(gettext_lazy(error_messages_str))


###### POSSIBLE OPTIONS #####
    # list_display = ("__str__",)
    # list_display_links = ()
    # list_filter = ()
    # list_select_related = False
    # list_per_page = 100
    # list_max_show_all = 200
    # list_editable = ()
    # search_fields = ()
    # search_help_text = None
    # date_hierarchy = None
    # save_as = False
    # save_as_continue = True
    # save_on_top = False
    # paginator = Paginator
    # preserve_filters = True
    # inlines = ()

    # fieldsets = (
    #     (None, {"fields": ("username", "password")}),
    #     (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
    #     (
    #         _("Permissions"),
    #         {
    #             "fields": (
    #                 "is_active",
    #                 "is_staff",
    #                 "is_superuser",
    #                 "groups",
    #                 "user_permissions",
    #             ),
    #         },
    #     ),
    #     (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    # )
    #
    # add_fieldsets = (
    #     (
    #         None,
    #         {
    #             "classes": ("wide",),
    #             "fields": ("username", "password1", "password2"),
    #         },
    #     ),
    # )
