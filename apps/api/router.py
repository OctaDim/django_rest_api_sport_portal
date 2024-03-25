from django.urls import path, include

app_name = "router"

urlpatterns = [
    path('users/', include("apps.api.user.urls")),  # IMPORTANT: DON'T FORGET TO ADD .urls to the end
    path('administrators/', include("apps.api.administrator.urls")),
    path('clients/', include("apps.api.client.urls")),
    path('coaches/', include("apps.api.coach.urls")),

    path('departments/', include("apps.api.department.urls")),
    path('training_groups/', include("apps.api.training_group.urls")),
    path('clients_progress/', include("apps.api.group_client_progress.urls")),

    path('authentication_jwt/', include("apps.api.authentication_jwt.urls")),
    path('authentication/', include("apps.api.authentication.urls")),

    path('emotional_levels/', include("apps.api.emotional_level.urls")),
    path('satisfaction_levels/', include("apps.api.self_satisfaction_level.urls")),

    # path('client_statuses/', include("apps.api.client_status.urls")),

]
