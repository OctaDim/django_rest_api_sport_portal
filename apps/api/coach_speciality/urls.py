from django.urls import path

from apps.api.coach_speciality.views import (
                                  AllCoachSpecialitiesGenericList,
                                  CreateNewCoachSpecialityGenericCreate,
                                  CoachSpecialityByIdGenericRetrieveUpdate,
                                  CoachSpecialityByIdGenericRetrieveDestroy,
                                  )

app_name = "coach_specialities"

urlpatterns = [
   path("all_coach_specialities/",
         AllCoachSpecialitiesGenericList.as_view(),
         name="list-all-coach-specialities"),

    path("create_new_coach_speciality/",
         CreateNewCoachSpecialityGenericCreate.as_view(),
         name="create-new-coach-speciality"),

    path("coach_speciality_by_id_soft/<int:coach_speciality_id>/",
         CoachSpecialityByIdGenericRetrieveUpdate.as_view(),
         name="coach-speciality-by-id-soft"),

    path("coach_speciality_by_id_hard/<int:coach_speciality_id>/",
         CoachSpecialityByIdGenericRetrieveDestroy.as_view(),
         name="coach-speciality-by-id-hard"),

]
