from django.urls import path

from apps.api.training_year.views import (
                            AllTrainingYearsGenericList,
                            CreateNewTrainingYearGenericCreate,
                            TrainingYearByIdGenericRetrieveUpdate,
                            TrainingYearByIdGenericRetrieveDestroy,
                            )

app_name = "training_years"

urlpatterns = [
   path("all_training_years/",
         AllTrainingYearsGenericList.as_view(),
         name="list-all-training-years"),

    path("create_new_training_year/",
         CreateNewTrainingYearGenericCreate.as_view(),
         name="create-new-training-year"),

    path("training_year_by_id_soft/<int:training_year_id>/",
         TrainingYearByIdGenericRetrieveUpdate.as_view(),
         name="training-year-by-id-soft"),

    path("training_year_by_id_hard/<int:training_year_id>/",
         TrainingYearByIdGenericRetrieveDestroy.as_view(),
         name="training-year-by-id-hard"),

]
