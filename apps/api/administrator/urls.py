from django.urls import path

from apps.api.administrator.views import (AllAdministratorsGenericList,
                                   CreateNewAdministratorGenericCreate,
                                   AdministratorByIdGenericRetrieveUpdate,
                                   AdministratorByIdGenericRetrieveDestroy,
                                   )

app_name = "administrators"

urlpatterns = [
   path("all_administrators/",
         AllAdministratorsGenericList.as_view(),
         name="list_all-administrators"),

    path("create_new_administrator/",
         CreateNewAdministratorGenericCreate.as_view(),
         name="create-new-administrator"),

    path("administrator_by_id_soft/<int:administrator_id>/",
         AdministratorByIdGenericRetrieveUpdate.as_view(),
         name="administrator-by-id-soft"),

    path("administrator_by_id_hard/<int:administrator_id>/",
         AdministratorByIdGenericRetrieveDestroy.as_view(),
         name="administrator-by-id-hard"),
]
