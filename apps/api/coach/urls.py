from django.urls import path

from apps.api.coach.views import (AllCoachesGenericList,
                                   CreateNewCoachGenericCreate,
                                   CoachByIdGenericRetrieveUpdate,
                                   CoachByIdGenericRetrieveDestroy,
                                   )

app_name = "coaches"

urlpatterns = [
   path("all_coaches/",
         AllCoachesGenericList.as_view(),
         name="list_all-coaches"),

    path("create_new_coach/",
         CreateNewCoachGenericCreate.as_view(),
         name="create-new-coach"),

    path("coach_by_id_soft/<int:coach_id>/",
         CoachByIdGenericRetrieveUpdate.as_view(),
         name="coach-by-id-soft"),

    path("coach_by_id_hard/<int:coach_id>/",
         CoachByIdGenericRetrieveDestroy.as_view(),
         name="coach-by-id-hard"),
]
