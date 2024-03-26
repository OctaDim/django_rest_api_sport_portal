from django.urls import path

from apps.api.gender.views import (AllGendersGenericList,
                                   CreateNewGenderGenericCreate,
                                   GenderByIdGenericRetrieveUpdate,
                                   GenderByIdGenericRetrieveDestroy,
                                   )

app_name = "genders"

urlpatterns = [
   path("all_genders/",
         AllGendersGenericList.as_view(),
         name="list-all-genders"),

    path("create_new_gender/",
         CreateNewGenderGenericCreate.as_view(),
         name="create-new-gender"),

    path("gender_by_id_soft/<int:gender_id>/",
         GenderByIdGenericRetrieveUpdate.as_view(),
         name="gender-by-id-soft"),

    path("gender_by_id_hard/<int:gender_id>/",
         GenderByIdGenericRetrieveDestroy.as_view(),
         name="gender-by-id-hard"),

]
