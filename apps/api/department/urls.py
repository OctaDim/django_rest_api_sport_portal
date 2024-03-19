from django.urls import path

from apps.api.department.views import (
                                    AllDepartmentsGenericList,
                                    CreateNewDepartmentGenericCreate,
                                    DepartmentByIdGenericRetrieveUpdate,
                                    DepartmentByIdGenericRetrieveDestroy,
                                    )
# #
app_name = "departments"

urlpatterns = [
   path("all_departments/",
         AllDepartmentsGenericList.as_view(),
         name="list_all-departments"),

    path("create_new_department/",
         CreateNewDepartmentGenericCreate.as_view(),
         name="create-new-department"),

    path("department_by_id_soft/<int:department_id>/",
         DepartmentByIdGenericRetrieveUpdate.as_view(),
         name="department-by-id-soft"),

    path("department_by_id_hard/<int:department_id>/",
         DepartmentByIdGenericRetrieveDestroy.as_view(),
         name="department-by-id-hard"),

]
