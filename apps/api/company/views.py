from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_COMPANIES_MSG,
                                                    ALL_COMPANIES_MSG,
                                                    COMPANY_CREATED_MSG,
                                                    COMPANY_NOT_CREATED_MSG,
                                                    NO_COMPANY_WITH_ID_MSG,
                                                    COMPANY_DETAILS,
                                                    COMPANY_UPDATED_MSG,
                                                    COMPANY_NOT_UPDATED_MSG,
                                                    COMPANY_DELETED_MSG
                                                    )

from apps.api.messages_api.messages_errors import (
                                    NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)

from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveDestroyAPIView,
                                     )

from apps.api.company.serializers import (
                        CompanyAllFieldsModelSerializer,
                        CompanyCreateModelSerializer,
                        CompanyRetrieveUpdateDeleteModelSerializer)

from apps.api.company.models import Company

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from apps.api.authentication.permissions_custom import (IsSuperuser,
                                                        IsAdministrator,
                                                        IsCoach,
                                                        IsClient,
                                                        IsActive,
                                                        IsVerified)


class AllCompaniesGenericList(ListAPIView):
    serializer_class = CompanyAllFieldsModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_queryset(self):
        companies = Company.objects.filter()
        return companies

    def get(self, request: Request, *args, **kwargs):
        companies = self.get_queryset()

        if not companies:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_COMPANIES_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=companies,
                                           many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_COMPANIES_MSG),
                              "data": serializer.data}
                        )



class CreateNewCompanyGenericCreate(CreateAPIView):
    serializer_class = CompanyCreateModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(COMPANY_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(COMPANY_NOT_CREATED_MSG),
                              "data": serializer.errors})



class CompanyByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = CompanyRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self, *args, **kwargs):
        company_id = self.kwargs.get("company_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        company_object = get_object_or_404(Company,
                                                 id=company_id)  # As one dictionary object, with exception

        # company_object = Company.objects.filter(id=company_id).first()  # As one dictionary object, exception should be handled
        # company_object = Company.objects.filter(id=company_id)  # As list with a dictionary element, exception should be handled
        #
        # if not company_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_COMPANY_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return company_object

    def get(self, request, *args, **kwargs):
        company = self.get_object()

        serializer = self.serializer_class(instance=company,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=company,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(COMPANY_DETAILS),
                              "data": serializer.data})

    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        company = self.get_object()

        company_id = self.kwargs.get("company_id")
        serializer = self.serializer_class(
                            instance=company,
                            data=request.data,
                            partial=True,
                            context={"company_id": company_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(COMPANY_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(COMPANY_NOT_UPDATED_MSG),
                              "data": serializer.errors})

    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        company = self.get_object()

        company_id = self.kwargs.get("company_id")
        serializer = self.serializer_class(
                            instance=company,
                            data=request.data,
                            partial=True,
                            context={"company_id": company_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(COMPANY_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(COMPANY_NOT_UPDATED_MSG),
                              "data": serializer.errors})

class CompanyByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = CompanyRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self):
        company_id = self.kwargs.get("company_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        company_object = get_object_or_404(Company,
                                                 id=company_id)  # As one dictionary object, with exception

        # company_object = Company.objects.filter(id=company_id).first()  # As one dictionary object, exception should be handled
        # company_object = Company.objects.filter(id=company_id)  # As list with a dictionary element, exception should be handled
        #
        # if not company_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_COMPANY_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return company_object

    def get(self, request, *args, **kwargs):
        company = self.get_object()

        serializer = self.serializer_class(instance=company,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=company,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(COMPANY_DETAILS),
                              "data": serializer.data})

    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)})

        company = self.get_object()
        company.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(COMPANY_DELETED_MSG),
                              "data": {}
                              })
