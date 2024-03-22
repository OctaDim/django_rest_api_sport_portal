from django.urls import path

from apps.api.group_client_progress.views import (
    AllGroupsClientsProgressGenericList,
    CreateNewGroupClientProgressGenericCreate,
    GroupClientProgressByIdGenericRetrieveUpdate,
    GroupClientProgressByIdGenericRetrieveDestroy,
                                    )

app_name = "groups-clients-progress"

urlpatterns = [
    path("all_clients_progress/",
         AllGroupsClientsProgressGenericList.as_view(),
         name="list_all-clients-progress"),

    path("create_new_client_progress/",
         CreateNewGroupClientProgressGenericCreate.as_view(),
         name="create-new-client-progress"),

    path("client_progress_by_id_soft/<int:client_progress_id>/",
         GroupClientProgressByIdGenericRetrieveUpdate.as_view(),
         name="client-progress-by-id-soft"),

    path("client_progress_by_id_hard/<int:client_progress_id>/",
         GroupClientProgressByIdGenericRetrieveDestroy.as_view(),
         name="client-progress-by-id-hard"),
]
