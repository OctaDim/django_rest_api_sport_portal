from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_GENDERS_MSG,
                                                    ALL_GENDERS_MSG,
                                                    GENDER_CREATED_MSG,
                                                    GENDER_NOT_CREATED_MSG,
                                                    NO_GENDER_WITH_ID_MSG,
                                                    GENDER_DETAILS,
                                                    GENDER_UPDATED_MSG,
                                                    GENDER_NOT_UPDATED_MSG,
                                                    GENDER_DELETED_MSG
                                                    )

from apps.api.messages_api.messages_errors import (
                                    NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)

from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveDestroyAPIView,
                                     )

from apps.api.gender.serializers import (
                        GenderAllFieldsModelSerializer,
                        GenderCreateModelSerializer,
                        GenderRetrieveUpdateDeleteModelSerializer)

from apps.api.gender.models import Gender

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from apps.api.authentication.permissions_custom import (IsSuperuser,
                                                        IsAdministrator,
                                                        IsCoach,
                                                        IsClient,
                                                        IsActive,
                                                        IsVerified)


class AllGendersGenericList(ListAPIView):
    serializer_class = GenderAllFieldsModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_queryset(self):
        companies = Gender.objects.filter()
        return companies

    def get(self, request: Request, *args, **kwargs):
        companies = self.get_queryset()

        if not companies:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_GENDERS_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=companies,
                                           many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_GENDERS_MSG),
                              "data": serializer.data}
                        )



class CreateNewGenderGenericCreate(CreateAPIView):
    serializer_class = GenderCreateModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(GENDER_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(GENDER_NOT_CREATED_MSG),
                              "data": serializer.errors})



class GenderByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = GenderRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self, *args, **kwargs):
        gender_id = self.kwargs.get("gender_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        gender_object = get_object_or_404(Gender,
                                                 id=gender_id)  # As one dictionary object, with exception

        # gender_object = Gender.objects.filter(id=gender_id).first()  # As one dictionary object, exception should be handled
        # gender_object = Gender.objects.filter(id=gender_id)  # As list with a dictionary element, exception should be handled
        #
        # if not gender_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_GENDER_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return gender_object

    def get(self, request, *args, **kwargs):
        gender = self.get_object()

        serializer = self.serializer_class(instance=gender,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=gender,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(GENDER_DETAILS),
                              "data": serializer.data})

    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        gender = self.get_object()

        gender_id = self.kwargs.get("gender_id")
        serializer = self.serializer_class(
                            instance=gender,
                            data=request.data,
                            partial=True,
                            context={"gender_id": gender_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(GENDER_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(GENDER_NOT_UPDATED_MSG),
                              "data": serializer.errors})

    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        gender = self.get_object()

        gender_id = self.kwargs.get("gender_id")
        serializer = self.serializer_class(
                            instance=gender,
                            data=request.data,
                            partial=True,
                            context={"gender_id": gender_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(GENDER_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(GENDER_NOT_UPDATED_MSG),
                              "data": serializer.errors})

class GenderByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = GenderRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self):
        gender_id = self.kwargs.get("gender_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        gender_object = get_object_or_404(Gender,
                                                 id=gender_id)  # As one dictionary object, with exception

        # gender_object = Gender.objects.filter(id=gender_id).first()  # As one dictionary object, exception should be handled
        # gender_object = Gender.objects.filter(id=gender_id)  # As list with a dictionary element, exception should be handled
        #
        # if not gender_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_GENDER_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return gender_object

    def get(self, request, *args, **kwargs):
        gender = self.get_object()

        serializer = self.serializer_class(instance=gender,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=gender,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(GENDER_DETAILS),
                              "data": serializer.data})

    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)})

        gender = self.get_object()
        gender.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(GENDER_DELETED_MSG),
                              "data": {}
                              })
