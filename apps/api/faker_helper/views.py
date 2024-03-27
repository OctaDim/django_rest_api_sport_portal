from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import (permission_classes,
                                       api_view)

from rest_framework.permissions import IsAuthenticated

from apps.api.authentication.permissions_custom import IsSuperuser

from apps.api.country.models import Country
from apps.api.company.models import Company

from faker import Faker



@api_view(["GET"])
@permission_classes([IsAuthenticated, IsSuperuser])
def generate_test_data_by_faker(request: Request):
    faker = Faker()
    records_number_required = 15


    ####################### Random Country #############################
    country_objects_count = Country.objects.all().count()
    for _ in range(0, records_number_required - country_objects_count):
        fake_name = "_"+faker.unique.country().upper()

        Country.objects.create(name= fake_name,
                               creator= request.user)


    ####################### Random Company #############################
    company_objects_count = Company.objects.all().count()
    for _ in range(0, records_number_required - company_objects_count):
        fake_name = "_"+faker.unique.company().upper()

        Company.objects.create(name= fake_name,
                               creator= request.user)

    return Response(status=status.HTTP_200_OK,
                    data = {"message": "Random values were generated"})
