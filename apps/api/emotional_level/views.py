# Create your views here.
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_EMOTIONAL_LEVELS_MSG,
                                                    ALL_EMOTIONAL_LEVELS_MSG,
                                                    EMOTIONAL_LEVEL_CREATED_MSG,
                                                    EMOTIONAL_LEVEL_NOT_CREATED_MSG,
                                                    NO_EMOTIONAL_LEVEL_WITH_ID_MSG,
                                                    EMOTIONAL_LEVEL_DETAILS,
                                                    EMOTIONAL_LEVEL_UPDATED_MSG,
                                                    EMOTIONAL_LEVEL_NOT_UPDATED_MSG,
                                                    EMOTIONAL_LEVEL_DELETED_MSG
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

from apps.api.emotional_level.serializers import (
    EmotionalLevelAllFieldsModelSerializer,
    EmotionalLevelCreateModelSerializer,
    EmotionalLevelRetrieveUpdateDeleteModelSerializer,
)

from apps.api.emotional_level.models import EmotionalLevel

from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from apps.api.authentication.permissions_custom import (IsSuperuser,
                                                        IsAdministrator,
                                                        IsCoach,
                                                        IsClient,
                                                        IsActive,
                                                        IsVerified)

# from rest_framework_simplejwt.authentication import JWTAuthentication



class AllEmotionalLevelsGenericList(ListAPIView):
    serializer_class = EmotionalLevelAllFieldsModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_queryset(self):
        emotional_levels = EmotionalLevel.objects.filter()
        return emotional_levels

    def get(self, request: Request, *args, **kwargs):
        emotional_levels = self.get_queryset()

        if not emotional_levels:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_EMOTIONAL_LEVELS_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=emotional_levels,
                                           many=True)  # IMPORTANT: DON'T FORGET many=True

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_EMOTIONAL_LEVELS_MSG),
                              "data": serializer.data}
                        )



class CreateNewEmotionalLevelGenericCreate(CreateAPIView):
    serializer_class = EmotionalLevelCreateModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(EMOTIONAL_LEVEL_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(EMOTIONAL_LEVEL_NOT_CREATED_MSG),
                              "data": serializer.errors})



class EmotionalLevelByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = EmotionalLevelRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self, *args, **kwargs):
        emotional_level_id = self.kwargs.get("emotional_level_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        emotional_level_object = get_object_or_404(EmotionalLevel,
                                                 id=emotional_level_id)  # As one dictionary object, with exception

        # emotional_level_object = EmotionalLevel.objects.filter(id=emotional_level_id).first()  # As one dictionary object, exception should be handled
        # emotional_level_object = EmotionalLevel.objects.filter(id=emotional_level_id)  # As list with a dictionary element, exception should be handled
        #
        # if not emotional_level_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_EMOTIONAL_LEVEL_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return emotional_level_object

    def get(self, request, *args, **kwargs):
        emotional_level = self.get_object()

        serializer = self.serializer_class(instance=emotional_level,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=emotional_level,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(EMOTIONAL_LEVEL_DETAILS),
                              "data": serializer.data})

    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        emotional_level = self.get_object()

        emotional_level_id = self.kwargs.get("emotional_level_id")
        serializer = self.serializer_class(
                            instance=emotional_level,
                            data=request.data,
                            partial=True,
                            context={"emotional_level_id": emotional_level_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(EMOTIONAL_LEVEL_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(EMOTIONAL_LEVEL_NOT_UPDATED_MSG),
                              "data": serializer.errors})

    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        emotional_level = self.get_object()

        emotional_level_id = self.kwargs.get("emotional_level_id")
        serializer = self.serializer_class(
                            instance=emotional_level,
                            data=request.data,
                            partial=True,
                            context={"emotional_level_id": emotional_level_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(EMOTIONAL_LEVEL_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(EMOTIONAL_LEVEL_NOT_UPDATED_MSG),
                              "data": serializer.errors})

class EmotionalLevelByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = EmotionalLevelRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self):
        emotional_level_id = self.kwargs.get("emotional_level_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        emotional_level_object = get_object_or_404(EmotionalLevel,
                                                 id=emotional_level_id)  # As one dictionary object, with exception

        # emotional_level_object = EmotionalLevel.objects.filter(id=emotional_level_id).first()  # As one dictionary object, exception should be handled
        # emotional_level_object = EmotionalLevel.objects.filter(id=emotional_level_id)  # As list with a dictionary element, exception should be handled
        #
        # if not emotional_level_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_EMOTIONAL_LEVEL_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return emotional_level_object

    def get(self, request, *args, **kwargs):
        emotional_level = self.get_object()

        serializer = self.serializer_class(instance=emotional_level,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=emotional_level,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(EMOTIONAL_LEVEL_DETAILS),
                              "data": serializer.data})

    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)})

        emotional_level = self.get_object()
        emotional_level.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(EMOTIONAL_LEVEL_DELETED_MSG),
                              "data": {}
                              })
