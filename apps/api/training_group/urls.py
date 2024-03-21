from django.urls import path

from apps.api.training_group.views import (
                                    AllTrainingGroupsGenericList,
                                    CreateNewTrainingGroupGenericCreate,
                                    TrainingGroupByIdGenericRetrieveUpdate,
                                    TrainingGroupByIdGenericRetrieveDestroy,
                                    )
# #
app_name = "training_groups"

urlpatterns = [
   path("all_training_groups/",
         AllTrainingGroupsGenericList.as_view(),
         name="list_all-training-groups"),

    path("create_new_training_group/",
         CreateNewTrainingGroupGenericCreate.as_view(),
         name="create-new-training-group"),

    path("training_group_by_id_soft/<int:training_group_id>/",
         TrainingGroupByIdGenericRetrieveUpdate.as_view(),
         name="training-group-by-id-soft"),

    path("training_group_by_id_hard/<int:training_group_id>/",
         TrainingGroupByIdGenericRetrieveDestroy.as_view(),
         name="training-group-by-id-hard"),

]
