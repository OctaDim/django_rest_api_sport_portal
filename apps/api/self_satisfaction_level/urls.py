from django.urls import path

from apps.api.self_satisfaction_level.views import (
                            AllSatisfactionLevelsGenericList,
                            CreateNewSatisfactionLevelGenericCreate,
                            SatisfactionLevelByIdGenericRetrieveUpdate,
                            SatisfactionLevelByIdGenericRetrieveDestroy,
                            )

app_name = "satisfaction_level"

urlpatterns = [
   path("all_satisfaction_levels/",
         AllSatisfactionLevelsGenericList.as_view(),
         name="list-all-satisfaction-levels"),

    path("create_new_satisfaction_level/",
         CreateNewSatisfactionLevelGenericCreate.as_view(),
         name="create-new-satisfaction-level"),

    path("satisfaction_level_by_id_soft/<int:satisfaction_level_id>/",
         SatisfactionLevelByIdGenericRetrieveUpdate.as_view(),
         name="satisfaction-level-by-id-soft"),

    path("satisfaction_level_by_id_hard/<int:satisfaction_level_id>/",
         SatisfactionLevelByIdGenericRetrieveDestroy.as_view(),
         name="satisfaction-level-by-id-hard"),

]
