from django.contrib import admin
# Register your models here.

from apps.api.department.models import Department

@admin.register(Department)  # Option 1
# admin.site.register(Department)  # Option 2
class DepartmentAdmin(admin.ModelAdmin):
    fields = ["name",
              "is_active",
              "company",
              "administrator",
              "address",
              "description",
              "note",
              "creator",
              ]

    list_display = ["id",
                    "name",
                    "company",
                    "administrator",
                    "address",
                    "description",
                    "note",
                    "is_active",
                    "created_at",
                    "updated_at",
                    "creator",
                    ]

    list_filter = ["company",
                   "administrator",
                   "is_active",
                   "created_at",
                   "updated_at",
                   "creator",
                   ]

    search_fields = ["id",
                     "name",
                     "company",
                     "administrator",
                     "address",
                     "description",
                     "note",
                     "is_active",
                     "created_at",
                     "updated_at",
                     "creator",
                    ]



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
