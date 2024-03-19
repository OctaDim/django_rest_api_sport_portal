from django.urls import path, include

app_name = "router"

urlpatterns = [
    path('users/', include("apps.api.user.urls")),  # IMPORTANT: DON'T FORGET TO ADD .urls to the end
    path('administrators/', include("apps.api.administrator.urls")),
    path('clients/', include("apps.api.client.urls")),
    path('coaches/', include("apps.api.coach.urls")),
    path('departments/', include("apps.api.department.urls")),
    path('clients_progress/', include("apps.api.group_client_progress.urls")),

]
