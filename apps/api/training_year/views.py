from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_TRAINING_YEARS_MSG,
                                                    ALL_TRAINING_YEARS_MSG,
                                                    TRAINING_YEAR_CREATED_MSG,
                                                    TRAINING_YEAR_NOT_CREATED_MSG,
                                                    NO_TRAINING_YEAR_WITH_ID_MSG,
                                                    TRAINING_YEAR_DETAILS,
                                                    TRAINING_YEAR_UPDATED_MSG,
                                                    TRAINING_YEAR_NOT_UPDATED_MSG,
                                                    TRAINING_YEAR_DELETED_MSG
                                                    )

from apps.api.messages_api.messages_errors import (
                                    NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)

from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveDestroyAPIView,
                                     )

from apps.api.training_year.serializers import (
                        TrainingYearAllFieldsModelSerializer,
                        TrainingYearCreateModelSerializer,
                        TrainingYearRetrieveUpdateDeleteModelSerializer)

from apps.api.training_year.models import TrainingYear

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from apps.api.authentication.permissions_custom import (IsSuperuser,
                                                        IsAdministrator,
                                                        IsCoach,
                                                        IsClient,
                                                        IsActive,
                                                        IsVerified)


class AllTrainingYearsGenericList(ListAPIView):
    serializer_class = TrainingYearAllFieldsModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_queryset(self):
        companies = TrainingYear.objects.filter()
        return companies

    def get(self, request: Request, *args, **kwargs):
        companies = self.get_queryset()

        if not companies:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_TRAINING_YEARS_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=companies,
                                           many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_TRAINING_YEARS_MSG),
                              "data": serializer.data}
                        )



class CreateNewTrainingYearGenericCreate(CreateAPIView):
    serializer_class = TrainingYearCreateModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(TRAINING_YEAR_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(TRAINING_YEAR_NOT_CREATED_MSG),
                              "data": serializer.errors})



class TrainingYearByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = TrainingYearRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self, *args, **kwargs):
        training_year_id = self.kwargs.get("training_year_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        training_year_object = get_object_or_404(TrainingYear,
                                                 id=training_year_id)  # As one dictionary object, with exception

        # training_year_object = TrainingYear.objects.filter(id=training_year_id).first()  # As one dictionary object, exception should be handled
        # training_year_object = TrainingYear.objects.filter(id=training_year_id)  # As list with a dictionary element, exception should be handled
        #
        # if not training_year_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_TRAINING_YEAR_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return training_year_object

    def get(self, request, *args, **kwargs):
        training_year = self.get_object()

        serializer = self.serializer_class(instance=training_year,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=training_year,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(TRAINING_YEAR_DETAILS),
                              "data": serializer.data})

    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        training_year = self.get_object()

        training_year_id = self.kwargs.get("training_year_id")
        serializer = self.serializer_class(
                            instance=training_year,
                            data=request.data,
                            partial=True,
                            context={"training_year_id": training_year_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(TRAINING_YEAR_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(TRAINING_YEAR_NOT_UPDATED_MSG),
                              "data": serializer.errors})

    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        training_year = self.get_object()

        training_year_id = self.kwargs.get("training_year_id")
        serializer = self.serializer_class(
                            instance=training_year,
                            data=request.data,
                            partial=True,
                            context={"training_year_id": training_year_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(TRAINING_YEAR_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(TRAINING_YEAR_NOT_UPDATED_MSG),
                              "data": serializer.errors})

class TrainingYearByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = TrainingYearRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self):
        training_year_id = self.kwargs.get("training_year_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        training_year_object = get_object_or_404(TrainingYear,
                                                 id=training_year_id)  # As one dictionary object, with exception

        # training_year_object = TrainingYear.objects.filter(id=training_year_id).first()  # As one dictionary object, exception should be handled
        # training_year_object = TrainingYear.objects.filter(id=training_year_id)  # As list with a dictionary element, exception should be handled
        #
        # if not training_year_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_TRAINING_YEAR_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return training_year_object

    def get(self, request, *args, **kwargs):
        training_year = self.get_object()

        serializer = self.serializer_class(instance=training_year,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=training_year,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(TRAINING_YEAR_DETAILS),
                              "data": serializer.data})

    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)})

        training_year = self.get_object()
        training_year.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(TRAINING_YEAR_DELETED_MSG),
                              "data": {}
                              })
