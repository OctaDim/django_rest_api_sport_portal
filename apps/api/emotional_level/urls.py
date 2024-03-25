from django.urls import path

from apps.api.emotional_level.views import (
                                  AllEmotionalLevelsGenericList,
                                  CreateNewEmotionalLevelGenericCreate,
                                  EmotionalLevelByIdGenericRetrieveUpdate,
                                  EmotionalLevelByIdGenericRetrieveDestroy,
                                  )

app_name = "emotional_level"

urlpatterns = [
   path("all_emotional_levels/",
         AllEmotionalLevelsGenericList.as_view(),
         name="list_all-emotional-levels"),

    path("create_new_emotional_level/",
         CreateNewEmotionalLevelGenericCreate.as_view(),
         name="create-new-emotional-level"),

    path("emotional_level_by_id_soft/<int:emotional_level_id>/",
         EmotionalLevelByIdGenericRetrieveUpdate.as_view(),
         name="emotional-level-by-id-soft"),

    path("emotional_level_by_id_hard/<int:emotional_level_id>/",
         EmotionalLevelByIdGenericRetrieveDestroy.as_view(),
         name="emotional-level-by-id-hard"),

]
