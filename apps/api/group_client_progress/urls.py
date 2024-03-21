from django.urls import path

from apps.api.group_client_progress.views import (
                                    AllClientsProgressGenericList,
                                    CreateNewClientProgressGenericCreate,
                                    ClientProgressByIdGenericRetrieveUpdate,
                                    ClientProgressByIdGenericRetrieveDestroy,
                                    )

app_name = "group-clients-progress"

urlpatterns = [
    path("all_clients_progress/",
          AllClientsProgressGenericList.as_view(),
          name="list_all-clients-progress"),

    # path("create_new_client_progress/",
    #      CreateNewClientProgressGenericCreate.as_view(),
    #      name="create-new-client-progress"),
    #
    # path("client_progress_by_id_soft/<int:client_progress_id>/",
    #      ClientProgressByIdGenericRetrieveUpdate.as_view(),
    #      name="client-progress-by-id-soft"),
    #
    # path("client_progress_by_id_hard/<int:client_progress_id>/",
    #      ClientProgressByIdGenericRetrieveDestroy.as_view(),
    #      name="client-progress-by-id-hard"),
]
