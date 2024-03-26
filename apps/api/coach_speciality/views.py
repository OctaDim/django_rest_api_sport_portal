from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_COACH_SPECIALITIES_MSG,
                                                    ALL_COACH_SPECIALITIES_MSG,
                                                    COACH_SPECIALITY_CREATED_MSG,
                                                    COACH_SPECIALITY_NOT_CREATED_MSG,
                                                    NO_COACH_SPECIALITY_WITH_ID_MSG,
                                                    COACH_SPECIALITY_DETAILS,
                                                    COACH_SPECIALITY_UPDATED_MSG,
                                                    COACH_SPECIALITY_NOT_UPDATED_MSG,
                                                    COACH_SPECIALITY_DELETED_MSG
                                                    )

from apps.api.messages_api.messages_errors import (
                                    NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)

from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveDestroyAPIView,
                                     )

from apps.api.coach_speciality.serializers import (
                        CoachSpecialityAllFieldsModelSerializer,
                        CoachSpecialityCreateModelSerializer,
                        CoachSpecialityRetrieveUpdateDeleteModelSerializer)

from apps.api.coach_speciality.models import CoachSpeciality

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from apps.api.authentication.permissions_custom import (IsSuperuser,
                                                        IsAdministrator,
                                                        IsCoach,
                                                        IsClient,
                                                        IsActive,
                                                        IsVerified)


class AllCoachSpecialitiesGenericList(ListAPIView):
    serializer_class = CoachSpecialityAllFieldsModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_queryset(self):
        coach_specialities = CoachSpeciality.objects.filter()
        return coach_specialities

    def get(self, request: Request, *args, **kwargs):
        coach_specialities = self.get_queryset()

        if not coach_specialities:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_COACH_SPECIALITIES_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=coach_specialities,
                                           many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_COACH_SPECIALITIES_MSG),
                              "data": serializer.data}
                        )



class CreateNewCoachSpecialityGenericCreate(CreateAPIView):
    serializer_class = CoachSpecialityCreateModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(COACH_SPECIALITY_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(COACH_SPECIALITY_NOT_CREATED_MSG),
                              "data": serializer.errors})



class CoachSpecialityByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = CoachSpecialityRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self, *args, **kwargs):
        coach_speciality_id = self.kwargs.get("coach_speciality_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        coach_speciality_object = get_object_or_404(CoachSpeciality,
                                                 id=coach_speciality_id)  # As one dictionary object, with exception

        # coach_speciality_object = CoachSpeciality.objects.filter(id=coach_speciality_id).first()  # As one dictionary object, exception should be handled
        # coach_speciality_object = CoachSpeciality.objects.filter(id=coach_speciality_id)  # As list with a dictionary element, exception should be handled
        #
        # if not coach_speciality_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_COACH_SPECIALITY_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return coach_speciality_object

    def get(self, request, *args, **kwargs):
        coach_speciality = self.get_object()

        serializer = self.serializer_class(instance=coach_speciality,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=coach_speciality,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(COACH_SPECIALITY_DETAILS),
                              "data": serializer.data})

    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        coach_speciality = self.get_object()

        coach_speciality_id = self.kwargs.get("coach_speciality_id")
        serializer = self.serializer_class(
                            instance=coach_speciality,
                            data=request.data,
                            partial=True,
                            context={"coach_speciality_id": coach_speciality_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(COACH_SPECIALITY_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(COACH_SPECIALITY_NOT_UPDATED_MSG),
                              "data": serializer.errors})

    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        coach_speciality = self.get_object()

        coach_speciality_id = self.kwargs.get("coach_speciality_id")
        serializer = self.serializer_class(
                            instance=coach_speciality,
                            data=request.data,
                            partial=True,
                            context={"coach_speciality_id": coach_speciality_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(COACH_SPECIALITY_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(COACH_SPECIALITY_NOT_UPDATED_MSG),
                              "data": serializer.errors})

class CoachSpecialityByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = CoachSpecialityRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self):
        coach_speciality_id = self.kwargs.get("coach_speciality_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        coach_speciality_object = get_object_or_404(CoachSpeciality,
                                                 id=coach_speciality_id)  # As one dictionary object, with exception

        # coach_speciality_object = CoachSpeciality.objects.filter(id=coach_speciality_id).first()  # As one dictionary object, exception should be handled
        # coach_speciality_object = CoachSpeciality.objects.filter(id=coach_speciality_id)  # As list with a dictionary element, exception should be handled
        #
        # if not coach_speciality_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_COACH_SPECIALITY_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return coach_speciality_object

    def get(self, request, *args, **kwargs):
        coach_speciality = self.get_object()

        serializer = self.serializer_class(instance=coach_speciality,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=coach_speciality,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(COACH_SPECIALITY_DETAILS),
                              "data": serializer.data})

    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)})

        coach_speciality = self.get_object()
        coach_speciality.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(COACH_SPECIALITY_DELETED_MSG),
                              "data": {}
                              })
