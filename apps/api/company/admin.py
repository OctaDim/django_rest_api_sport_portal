from django.contrib import admin

from django.utils.translation import gettext_lazy
from django.contrib import messages
from django.db.models import Q

from apps.api.messages_api.messages_actions import (
    COMPANY_CREATOR_IS_CURRENT_USER)

from apps.api.user.models import User

from apps.api.company.models import Company



@admin.register(Company)  # Option 1
# admin.site.register(Company)  # Option 2
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["id",
                    "name",
                    "description",
                    "is_active",
                    "created_at",
                    "updated_at",
                    "creator",
                    ]

    list_filter = ["id",
                   "name",
                   "description",
                   "is_active",
                   "created_at",
                    "updated_at",
                    "creator",
                   ]

    search_fields = ["id",
                     "name",
                     "description",
                     "is_active",
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
                          COMPANY_CREATOR_IS_CURRENT_USER))
        super().save_model(request, obj, form, change)
