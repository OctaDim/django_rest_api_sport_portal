from django.urls import path

from apps.api.company.views import (AllCompaniesGenericList,
                                    CreateNewCompanyGenericCreate,
                                    CompanyByIdGenericRetrieveUpdate,
                                    CompanyByIdGenericRetrieveDestroy,
                                    )

app_name = "companies"

urlpatterns = [
   path("all_companies/",
         AllCompaniesGenericList.as_view(),
         name="list-all-companies"),

    path("create_new_company/",
         CreateNewCompanyGenericCreate.as_view(),
         name="create-new-company"),

    path("company_by_id_soft/<int:company_id>/",
         CompanyByIdGenericRetrieveUpdate.as_view(),
         name="company-by-id-soft"),

    path("company_by_id_hard/<int:company_id>/",
         CompanyByIdGenericRetrieveDestroy.as_view(),
         name="company-by-id-hard"),

]
