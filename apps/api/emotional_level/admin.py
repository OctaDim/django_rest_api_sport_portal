from django.contrib import admin
# Register your models here.

from apps.api.emotional_level.models import EmotionalLevel

@admin.register(EmotionalLevel)  # Option 1
# admin.site.register(EmotionalLevel)  # Option 2
class EmotionalLevelAdmin(admin.ModelAdmin):
    list_display = ["id",
                    "value",
                    "name",
                    "description",
                    "icon_link",
                    "created_at",
                    "updated_at",
                    "creator",
                    ]

    list_filter = ["id",
                   "value",
                   "name",
                   "description",
                   "icon_link",
                   "created_at",
                   "updated_at",
                   "creator",
                   ]

    search_fields = ["id",
                     "value",
                     "name",
                     "description",
                     "icon_link",
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
