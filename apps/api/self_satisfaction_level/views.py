# Create your views here.
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_SATISFACTION_LEVELS_MSG,
                                                    ALL_SATISFACTION_LEVELS_MSG,
                                                    SATISFACTION_LEVEL_CREATED_MSG,
                                                    SATISFACTION_LEVEL_NOT_CREATED_MSG,
                                                    NO_SATISFACTION_LEVEL_WITH_ID_MSG,
                                                    SATISFACTION_LEVEL_DETAILS,
                                                    SATISFACTION_LEVEL_UPDATED_MSG,
                                                    SATISFACTION_LEVEL_NOT_UPDATED_MSG,
                                                    SATISFACTION_LEVEL_DELETED_MSG
                                                    )

from apps.api.messages_api.messages_errors import (NOT_SUPERUSER_HARD_DELETE_FORBIDDEN,
                                                   NOT_SUPERUSER_FORBIDDEN,
                                                   DELETE_YOURSELF_FORBIDDEN,
                                                   INACTIVE_YOURSELF_FORBIDDEN,
                                                   )

from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveDestroyAPIView,
                                     )

from apps.api.self_satisfaction_level.serializers import (
    SatisfactionLevelAllFieldsModelSerializer,
    SatisfactionLevelCreateModelSerializer,
    SatisfactionLevelRetrieveUpdateDeleteModelSerializer,
)

from apps.api.self_satisfaction_level.models import SelfSatisfactionLevel

from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from apps.api.authentication.permissions_custom import (IsSuperuser,
                                                        IsAdministrator,
                                                        IsCoach,
                                                        IsClient,
                                                        IsActive,
                                                        IsVerified)

# from rest_framework_simplejwt.authentication import JWTAuthentication



class AllSatisfactionLevelsGenericList(ListAPIView):
    serializer_class = SatisfactionLevelAllFieldsModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_queryset(self):
        satisfaction_levels = SelfSatisfactionLevel.objects.filter()
        return satisfaction_levels

    def get(self, request: Request, *args, **kwargs):
        satisfaction_levels = self.get_queryset()

        if not satisfaction_levels:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_SATISFACTION_LEVELS_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=satisfaction_levels,
                                           many=True)  # IMPORTANT: DON'T FORGET many=True

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_SATISFACTION_LEVELS_MSG),
                              "data": serializer.data}
                        )



class CreateNewSatisfactionLevelGenericCreate(CreateAPIView):
    serializer_class = SatisfactionLevelCreateModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(SATISFACTION_LEVEL_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(SATISFACTION_LEVEL_NOT_CREATED_MSG),
                              "data": serializer.errors})



class SatisfactionLevelByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = SatisfactionLevelRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self, *args, **kwargs):
        satisfaction_level_id = self.kwargs.get("satisfaction_level_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        satisfaction_level_object = get_object_or_404(SelfSatisfactionLevel,
                                                 id=satisfaction_level_id)  # As one dictionary object, with exception

        # satisfaction_level_object = SatisfactionLevel.objects.filter(id=satisfaction_level_id).first()  # As one dictionary object, exception should be handled
        # satisfaction_level_object = SatisfactionLevel.objects.filter(id=satisfaction_level_id)  # As list with a dictionary element, exception should be handled
        #
        # if not satisfaction_level_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_SATISFACTION_LEVEL_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return satisfaction_level_object

    def get(self, request, *args, **kwargs):
        satisfaction_level = self.get_object()

        serializer = self.serializer_class(instance=satisfaction_level,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=satisfaction_level,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(SATISFACTION_LEVEL_DETAILS),
                              "data": serializer.data})

    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        satisfaction_level = self.get_object()

        satisfaction_level_id = self.kwargs.get("satisfaction_level_id")
        serializer = self.serializer_class(
                            instance=satisfaction_level,
                            data=request.data,
                            partial=True,
                            context={"satisfaction_level_id": satisfaction_level_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(SATISFACTION_LEVEL_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(SATISFACTION_LEVEL_NOT_UPDATED_MSG),
                              "data": serializer.errors})

    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        satisfaction_level = self.get_object()

        satisfaction_level_id = self.kwargs.get("satisfaction_level_id")
        serializer = self.serializer_class(
                            instance=satisfaction_level,
                            data=request.data,
                            partial=True,
                            context={"satisfaction_level_id": satisfaction_level_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(SATISFACTION_LEVEL_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(SATISFACTION_LEVEL_NOT_UPDATED_MSG),
                              "data": serializer.errors})

class SatisfactionLevelByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = SatisfactionLevelRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self):
        satisfaction_level_id = self.kwargs.get("satisfaction_level_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        satisfaction_level_object = get_object_or_404(SelfSatisfactionLevel,
                                                 id=satisfaction_level_id)  # As one dictionary object, with exception

        # satisfaction_level_object = SatisfactionLevel.objects.filter(id=satisfaction_level_id).first()  # As one dictionary object, exception should be handled
        # satisfaction_level_object = SatisfactionLevel.objects.filter(id=satisfaction_level_id)  # As list with a dictionary element, exception should be handled
        #
        # if not satisfaction_level_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_SATISFACTION_LEVEL_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return satisfaction_level_object

    def get(self, request, *args, **kwargs):
        satisfaction_level = self.get_object()

        serializer = self.serializer_class(instance=satisfaction_level,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=satisfaction_level,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(SATISFACTION_LEVEL_DETAILS),
                              "data": serializer.data})

    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)})

        satisfaction_level = self.get_object()
        satisfaction_level.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(SATISFACTION_LEVEL_DELETED_MSG),
                              "data": {}
                              })
