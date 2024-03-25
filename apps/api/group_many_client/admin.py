from django.contrib import admin
from django.utils.translation import gettext_lazy
from django.contrib import messages
from django.db.models import Q

from apps.api.messages_api.messages_actions import (
     GROUP_CLIENT_RECORD_CREATOR_IS_CURRENT_USER)

from apps.api.user.models import User

from apps.api.group_many_client.models import GroupManyClient



@admin.register(GroupManyClient)
class GroupManyClientAdmin(admin.ModelAdmin):
    # Defining fields and order to edit in the form and save
    # Possible to use all fields from the model by names defined in the model
    # <relative_table>__<field_name> does not work
    # fields = "__all__"
    fields = ["training_group_id",
              "client_id",
              "creator"
              ]

    # Table displaying fields. Defining order and ordering
    # Possible to use all fields by names from the model without ordering
    # To order model fields or relative fields methods+decorator @admin.display() is necessary
    # Direct access (as "country") to the relative fields is allowed ()
    # <relative_table>__<field_name> does not work
    list_display = ["id",
                    "training_group_id",
                    "client_id",
                    "created_at",
                    "updated_at",
                    "creator",
                    ]

    # All search fields defined as <relative_table>__<field_name> only
    # Impossible to use relative FK fields __str__
    # Direct access (as "country") to the relative fields is not allowed ()
    # search_fields = "__all__"
    search_fields = ["id",
                    "training_group_many__training_group_code",
                     "training_group_many__training_group_name",
                     "client_many__user__username",
                     "client_many__user__email",
                     "client_many__user__nickname",
                     "created_at",
                     "updated_at",
                     "creator__user__username",
                     "creator__user__email",
                     "creator__user__nickname",                    ]

    # All search fields defined as <relative_table>__<field_name> only
    # Possible to use relative FK fields __str__
    # Direct access (as "country") to the relative fields is allowed ()
    # list_filter = "__all__"
    list_filter = ["training_group_id",
                   "client_id",
                   "created_at",
                   "updated_at",
                   "creator",
                   ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):  # Values available to choice
        if (db_field.name == "creator"
                and request.user.is_authenticated):
                    kwargs["queryset"] = User.objects.filter(pk=request.user.pk)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def save_model(self, request, obj, form, change):  # Default value for new object
        obj.creator = User.objects.get(id=request.user.id)  # Creator must always be current user
        messages.info(request=request,
                      message=gettext_lazy(
                          GROUP_CLIENT_RECORD_CREATOR_IS_CURRENT_USER))
        super().save_model(request, obj, form, change)
