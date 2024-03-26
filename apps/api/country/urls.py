from django.urls import path

from apps.api.country.views import (AllCountriesGenericList,
                                    CreateNewCountryGenericCreate,
                                    CountryByIdGenericRetrieveUpdate,
                                    CountryByIdGenericRetrieveDestroy,
                                    )

app_name = "countries"

urlpatterns = [
   path("all_countries/",
         AllCountriesGenericList.as_view(),
         name="list-all-countries"),

    path("create_new_country/",
         CreateNewCountryGenericCreate.as_view(),
         name="create-new-country"),

    path("country_by_id_soft/<int:country_id>/",
         CountryByIdGenericRetrieveUpdate.as_view(),
         name="country-by-id-soft"),

    path("country_by_id_hard/<int:country_id>/",
         CountryByIdGenericRetrieveDestroy.as_view(),
         name="country-by-id-hard"),

]
