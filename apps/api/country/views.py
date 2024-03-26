from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_COUNTRIES_MSG,
                                                    ALL_COUNTRIES_MSG,
                                                    COUNTRY_CREATED_MSG,
                                                    COUNTRY_NOT_CREATED_MSG,
                                                    NO_COUNTRY_WITH_ID_MSG,
                                                    COUNTRY_DETAILS,
                                                    COUNTRY_UPDATED_MSG,
                                                    COUNTRY_NOT_UPDATED_MSG,
                                                    COUNTRY_DELETED_MSG
                                                    )

from apps.api.messages_api.messages_errors import (
                                    NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)

from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveDestroyAPIView,
                                     )

from apps.api.country.serializers import (
                        CountryAllFieldsModelSerializer,
                        CountryCreateModelSerializer,
                        CountryRetrieveUpdateDeleteModelSerializer)

from apps.api.country.models import Country

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from apps.api.authentication.permissions_custom import (IsSuperuser,
                                                        IsAdministrator,
                                                        IsCoach,
                                                        IsClient,
                                                        IsActive,
                                                        IsVerified)


class AllCountriesGenericList(ListAPIView):
    serializer_class = CountryAllFieldsModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_queryset(self):
        companies = Country.objects.filter()
        return companies

    def get(self, request: Request, *args, **kwargs):
        companies = self.get_queryset()

        if not companies:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_COUNTRIES_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=companies,
                                           many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_COUNTRIES_MSG),
                              "data": serializer.data}
                        )



class CreateNewCountryGenericCreate(CreateAPIView):
    serializer_class = CountryCreateModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(COUNTRY_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(COUNTRY_NOT_CREATED_MSG),
                              "data": serializer.errors})



class CountryByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = CountryRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self, *args, **kwargs):
        country_id = self.kwargs.get("country_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        country_object = get_object_or_404(Country,
                                                 id=country_id)  # As one dictionary object, with exception

        # country_object = Country.objects.filter(id=country_id).first()  # As one dictionary object, exception should be handled
        # country_object = Country.objects.filter(id=country_id)  # As list with a dictionary element, exception should be handled
        #
        # if not country_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_COUNTRY_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return country_object

    def get(self, request, *args, **kwargs):
        country = self.get_object()

        serializer = self.serializer_class(instance=country,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=country,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(COUNTRY_DETAILS),
                              "data": serializer.data})

    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        country = self.get_object()

        country_id = self.kwargs.get("country_id")
        serializer = self.serializer_class(
                            instance=country,
                            data=request.data,
                            partial=True,
                            context={"country_id": country_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(COUNTRY_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(COUNTRY_NOT_UPDATED_MSG),
                              "data": serializer.errors})

    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        country = self.get_object()

        country_id = self.kwargs.get("country_id")
        serializer = self.serializer_class(
                            instance=country,
                            data=request.data,
                            partial=True,
                            context={"country_id": country_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(COUNTRY_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(COUNTRY_NOT_UPDATED_MSG),
                              "data": serializer.errors})

class CountryByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = CountryRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self):
        country_id = self.kwargs.get("country_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        country_object = get_object_or_404(Country,
                                                 id=country_id)  # As one dictionary object, with exception

        # country_object = Country.objects.filter(id=country_id).first()  # As one dictionary object, exception should be handled
        # country_object = Country.objects.filter(id=country_id)  # As list with a dictionary element, exception should be handled
        #
        # if not country_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_COUNTRY_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return country_object

    def get(self, request, *args, **kwargs):
        country = self.get_object()

        serializer = self.serializer_class(instance=country,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=country,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(COUNTRY_DETAILS),
                              "data": serializer.data})

    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)})

        country = self.get_object()
        country.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(COUNTRY_DELETED_MSG),
                              "data": {}
                              })
