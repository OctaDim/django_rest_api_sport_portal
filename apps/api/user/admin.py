from django.contrib import admin
# Register your models here.

# ##################################################################
# from django.contrib.auth.models import User  # Django default user
from apps.api.user.models import User  # Custom user
# ##################################################################


@admin.register(User)
# admin.site.register(User)
class CustomUserCustomAdminPanel(admin.ModelAdmin):
    list_display = ["id",
                    "email",
                    "username",
                    "nickname",
                    "first_name",
                    "last_name",
                    "phone",
                    "is_staff",
                    "is_trainer",
                    "is_superuser",
                    "is_verified",
                    "is_active",
                    "date_joined",
                    "last_login",
                    "updated"
                    ]

    list_filter = ["is_staff",
                   "is_trainer",
                   "is_superuser",
                   "is_verified",
                   "is_active",
                   "date_joined",
                   "last_login",
                   "updated"
                   ]

    search_fields = ["id",
                    "email",
                    "username",
                    "nickname",
                    "first_name",
                    "last_name",
                    "phone",
                    "is_staff",
                    "is_trainer",
                    "is_superuser",
                    "is_verified",
                    "is_active",
                    "date_joined",
                    "last_login",
                    "updated"
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
