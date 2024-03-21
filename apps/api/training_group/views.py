# Create your views here.

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_TRAINING_GROUPS_MSG,
                                                    ALL_TRAINING_GROUPS_MSG,
                                                    TRAINING_GROUP_CREATED_MSG,
                                                    TRAINING_GROUP_NOT_CREATED_MSG,
                                                    NO_TRAINING_GROUP_WITH_ID_MSG,
                                                    TRAINING_GROUP_DETAILS,
                                                    TRAINING_GROUP_UPDATED_MSG,
                                                    TRAINING_GROUP_NOT_UPDATED_MSG,
                                                    TRAINING_GROUP_DELETED_MSG
                                                    )

from apps.api.messages_api.messages_errors import (NOT_SUPERUSER_HARD_DELETE_FORBIDDEN,
                                                   HARD_DELETE_FORBIDDEN_CLIENT_REFS_EXIST,
                                                   )

from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveDestroyAPIView,
                                     )

from apps.api.training_group.serializers import (
    TrainingGroupAllFieldsModelSerializer,
    TrainingGroupCreateModelSerializer,
    TrainingGroupRetrieveUpdateDeleteModelSerializer,
)

from apps.api.training_group.models import TrainingGroup
from apps.api.administrator.models import Administrator
from apps.api.client.models import Client
from apps.api.coach.models import Coach


from apps.api.user.models import User



class AllTrainingGroupsGenericList(ListAPIView):
    serializer_class = TrainingGroupAllFieldsModelSerializer

    def get_queryset(self):
        training_groups = TrainingGroup.objects.filter()
        return training_groups

    def get(self, request: Request, *args, **kwargs):
        training_groups = self.get_queryset()

        if not training_groups:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_TRAINING_GROUPS_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=training_groups, many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_TRAINING_GROUPS_MSG),
                              "data": serializer.data}
                        )



class CreateNewTrainingGroupGenericCreate(CreateAPIView):
    serializer_class = TrainingGroupCreateModelSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(TRAINING_GROUP_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(TRAINING_GROUP_NOT_CREATED_MSG),
                              "data": serializer.errors})



class TrainingGroupByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = TrainingGroupRetrieveUpdateDeleteModelSerializer

    def get_object(self, *args, **kwargs):
        training_group_id = self.kwargs.get("training_group_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        training_group_object = get_object_or_404(TrainingGroup,
                                                  id=training_group_id)  # As one dictionary object, with exception

        # training_group_object = TrainingGroup.objects.filter(id=training_group_id).first()  # As one dictionary object, exception should be handled
        # training_group_id_object = TrainingGroup.objects.filter(id=training_group_id)  # As list with a dictionary element, exception should be handled
        #
        # if not training_group_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_TRAINING_GROUP_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return training_group_object

    def get(self, request, *args, **kwargs):
        training_group = self.get_object()

        serializer = self.serializer_class(instance=training_group,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=training_group,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(TRAINING_GROUP_DETAILS),
                              "data": serializer.data})

    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        training_group = self.get_object()

        training_group_id = self.kwargs.get("training_group_id")
        serializer = self.serializer_class(
                            instance=training_group,
                            data=request.data,
                            partial=True,
                            context={"training_group_id": training_group_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(TRAINING_GROUP_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(TRAINING_GROUP_NOT_UPDATED_MSG),
                              "data": serializer.errors})

    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        training_group = self.get_object()

        training_group_id = self.kwargs.get("training_group_id")
        serializer = self.serializer_class(
                            instance=training_group,
                            data=request.data,
                            partial=True,
                            context={"training_group_id": training_group_id,  # Add transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(TRAINING_GROUP_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(TRAINING_GROUP_NOT_UPDATED_MSG),
                              "data": serializer.errors})



class TrainingGroupByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = TrainingGroupRetrieveUpdateDeleteModelSerializer

    def get_object(self):
        training_group_id = self.kwargs.get("training_group_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        training_group_object = get_object_or_404(TrainingGroup, id=training_group_id)  # As one dictionary object, with exception

        # training_group_object = TrainingGroup.objects.filter(id=training_group_id).first()  # As one dictionary object, exception should be handled
        # training_group_id_object = TrainingGroup.objects.filter(id=training_group_id)  # As list with a dictionary element, exception should be handled
        #
        # if not training_group_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_TRAINING_GROUP_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return training_group_object

    def get(self, request, *args, **kwargs):
        training_group = self.get_object()

        serializer = self.serializer_class(instance=training_group,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=training_group,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(TRAINING_GROUP_DETAILS),
                              "data": serializer.data})

    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)})

        training_group = self.get_object()
        if training_group.client.all().exists():
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(HARD_DELETE_FORBIDDEN_CLIENT_REFS_EXIST)})

        training_group = self.get_object()
        training_group.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(TRAINING_GROUP_DELETED_MSG),
                              "data": {}
                              })
