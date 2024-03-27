from django.urls import path, include

app_name = "router"

urlpatterns = [
    path('faker_helpers/', include("apps.api.faker_helper.urls")),

    path('authentication/', include("apps.api.authentication.urls")),  # IMPORTANT: DON'T FORGET TO ADD .urls to the end
    path('authentication_jwt/', include("apps.api.authentication_jwt.urls")),

    path('users/', include("apps.api.user.urls")),
    path('administrators/', include("apps.api.administrator.urls")),
    path('clients/', include("apps.api.client.urls")),
    path('coaches/', include("apps.api.coach.urls")),

    path('companies/', include("apps.api.company.urls")),
    path('departments/', include("apps.api.department.urls")),
    path('training_groups/', include("apps.api.training_group.urls")),
    path('clients_progress/', include("apps.api.group_client_progress.urls")),

    path('emotional_levels/', include("apps.api.emotional_level.urls")),
    path('satisfaction_levels/', include("apps.api.self_satisfaction_level.urls")),

    path('client_statuses/', include("apps.api.client_status.urls")),
    path('coach_specialities/', include("apps.api.coach_speciality.urls")),

    path('countries/', include("apps.api.country.urls")),
    path('genders/', include("apps.api.gender.urls")),
    path('payment_documents/', include("apps.api.payment_document.urls")),
    path('payment_types/', include("apps.api.payment_type.urls")),
    path('training_years/', include("apps.api.training_year.urls")),

]
