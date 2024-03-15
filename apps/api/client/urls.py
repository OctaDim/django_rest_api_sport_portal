from django.urls import path

from apps.api.client.views import (AllClientsGenericList,
                                   CreateNewClientGenericCreate,
                                   )

app_name = "clients"

urlpatterns = [
   path("all_clients/",
         AllClientsGenericList.as_view(),
         name="list_all-clients"),

    path("create_new_client/",
         CreateNewClientGenericCreate.as_view(), name="create-new-client"),

    # path("client_by_id_soft/<int:client_id>/",
    #      ClientByIdGenericRetrieveUpd.as_view(),
    #      name="client-by-id-soft"),
    #
    # path("client_by_id_hard/<int:user_id>/",
    #      ClientByIdGenericRetrieveUpdDestroy.as_view(),
    #      name="client-by-id-hard"),
]
