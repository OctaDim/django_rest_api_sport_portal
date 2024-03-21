from django.contrib import admin
# Register your models here.

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import PROGRESS_RECORD_CREATOR_IS_CURRENT_USER

from apps.api.group_client_progress.models import GroupClientProgress
from apps.api.user.models import User

from django.contrib import messages
from django.db.models import Q



@admin.register(GroupClientProgress)
class GroupClientProgressAdmin(admin.ModelAdmin):

    # Defining fields and order to edit in the form and save
    # Possible to use all fields from the model by names defined in the model
    # <relative_table>__<field_name> does not work
    fields = ["group_many_client",  # Form fields and order
              "self_satisfaction_level",
              "emotional_level",
              "task_completed",
              "check_point_date",
              "current_weight",
              "current_breast",
              "current_shoulders",
              "current_waist",
              "current_hips",
              "description",
              "note",
              "creator",
              ]

    # Table displaying fields. Defining order and ordering
    # Possible to use all fields by names from the model without ordering
    # To order model fields or relative fields methods+decorator @admin.display() is necessary
    # Direct access (as "country") to the relative fields is allowed ()
    # <relative_table>__<field_name> does not work
    list_display = ["id",  # Table fields and order
                    # "group_many_client__group_many_client__client_username",
                    "self_satisfaction_level",
                    "emotional_level",
                    "task_completed",
                    "check_point_date",
                    "current_weight",
                    "current_breast",
                    "current_shoulders",
                    "current_waist",
                    "current_hips",
                    "description",
                    "note",
                    "created_at",
                    "updated_at",
                    "creator",
                    ]

    # # All search fields defined as <relative_table>__<field_name> only
    # # Impossible to use relative FK fields __str__
    # # Direct access (as "country") to the relative fields is not allowed ()
    # # search_fields = "__all__"
    search_fields = ["id",
                    # "group_many_client__group_many_client__training_group_id",
                    #  "group_many_client__group_many_client__client_id",
                     "self_satisfaction_level__value",
                     "self_satisfaction_level__name",
                     "emotional_level__value",
                     "emotional_level__name",
                     "task_completed",
                     "check_point_date",
                     "current_weight",
                     "current_breast",
                     "current_shoulders",
                     "current_waist",
                     "current_hips",
                     "description",
                     "note",
                     "created_at",
                     "updated_at",
                     "creator__username",
                     "creator__email",
                     "creator__nickname",
                     ]

    # All filter fields defined as <relative_table>__<field_name> only
    # Possible to use relative FK fields __str__
    # Direct access (as "country") to the relative fields is allowed ()
    # list_filter = "__all__"
    list_filter = ["self_satisfaction_level",
                   "emotional_level",
                   "task_completed",
                   "check_point_date",
                   "creator",
                   ]

    # def __init__(self, model, admin_site):
    #     # self.list_display = [field.name for field in model._meta.get_fields()]
    #     # self.list_display.remove("administrator")
    #     # self.list_display.remove("client")
    #     # self.list_display.remove("coach")
    #     super().__init__(model, admin_site)

    # def get_queryset(self, request):
    #     # if request.user.is_trainer:
    #     #     return self.model.objects.none()
    #     query_set = super().get_queryset(request)
    #     return query_set

    def formfield_for_foreignkey(self, db_field, request, **kwargs):  # Values available to choice
        if (db_field.name == "creator"
                and request.user.is_authenticated):
                    kwargs["queryset"] = User.objects.filter(pk=request.user.pk)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def save_model(self, request, obj, form, change):  # Default value for new object
        obj.creator = User.objects.get(id=request.user.id)  # Creator must always be current user
        messages.info(request=request,
                      message=gettext_lazy(
                          PROGRESS_RECORD_CREATOR_IS_CURRENT_USER))
        super().save_model(request, obj, form, change)
