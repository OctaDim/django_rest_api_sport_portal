from django.urls import path

from apps.api.client_status.views import (
                                  AllClientStatusesGenericList,
                                  CreateNewClientStatusGenericCreate,
                                  ClientStatusByIdGenericRetrieveUpdate,
                                  ClientStatusByIdGenericRetrieveDestroy,
                                  )

app_name = "client_status"

urlpatterns = [
   path("all_client_statuses/",
         AllClientStatusesGenericList.as_view(),
         name="list-all-client-statuses"),

    path("create_new_client_status/",
         CreateNewClientStatusGenericCreate.as_view(),
         name="create-new-client-status"),

    path("client_status_by_id_soft/<int:client_status_id>/",
         ClientStatusByIdGenericRetrieveUpdate.as_view(),
         name="client-status-by-id-soft"),

    path("client_status_by_id_hard/<int:client_status_id>/",
         ClientStatusByIdGenericRetrieveDestroy.as_view(),
         name="client-status-by-id-hard"),

]
