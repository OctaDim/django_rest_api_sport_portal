from django.urls import path

from apps.api.faker_helper.views import generate_test_data_by_faker

app_name = "faker-helpers"



urlpatterns = [
   path("generate_test_data/",
        generate_test_data_by_faker,
        name="generate-test-data-by-faker"),

]
