# Create your views here.

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_CLIENTS_PROGRESS_MSG,
                                                    ALL_CLIENTS_PROGRESS_MSG,
                                                    CLIENT_PROGRESS_CREATED_MSG,
                                                    CLIENT_PROGRESS_NOT_CREATED_MSG,
                                                    NO_CLIENT_PROGRESS_WITH_ID_MSG,
                                                    CLIENT_PROGRESS_DETAILS,
                                                    CLIENT_PROGRESS_UPDATED_MSG,
                                                    CLIENT_PROGRESS_NOT_UPDATED_MSG,
                                                    CLIENT_PROGRESS_DELETED_MSG
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

from apps.api.group_client_progress.serializers import (
    GroupClientProgressAllFieldsModelSerializer,
    GroupClientProgressCreateModelSerializer,
    GroupClientProgressRetrieveUpdateDeleteModelSerializer,
                            )

from apps.api.group_client_progress.models import GroupClientProgress
from apps.api.user.models import User



class AllGroupsClientsProgressGenericList(ListAPIView):
    serializer_class = GroupClientProgressAllFieldsModelSerializer

    def get_queryset(self):
        groups_clients_progress = GroupClientProgress.objects.filter()
        return groups_clients_progress

    def get(self, request: Request, *args, **kwargs):
        groups_clients_progress = self.get_queryset()

        if not groups_clients_progress:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_CLIENTS_PROGRESS_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=groups_clients_progress,
                                           many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_CLIENTS_PROGRESS_MSG),
                              "data": serializer.data}
                        )



class CreateNewGroupClientProgressGenericCreate(CreateAPIView):
    serializer_class = GroupClientProgressCreateModelSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(CLIENT_PROGRESS_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(CLIENT_PROGRESS_NOT_CREATED_MSG),
                              "data": serializer.errors})



class GroupClientProgressByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = GroupClientProgressRetrieveUpdateDeleteModelSerializer

    def get_object(self, *args, **kwargs):
        client_progress_id = self.kwargs.get("client_progress_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        client_progress_object = get_object_or_404(GroupClientProgress,
                                                  id=client_progress_id)  # As one dictionary object, with exception

        # client_progress_object = GroupClientProgress.objects.filter(id=client_progress_id).first()  # As one dictionary object, exception should be handled
        # client_progress_object = GroupClientProgress.objects.filter(id=client_progress_id)  # As list with a dictionary element, exception should be handled
        #
        # if not client_progress_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_CLIENT_PROGRESS_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return client_progress_object

    def get(self, request, *args, **kwargs):
        client_progress = self.get_object()

        serializer = self.serializer_class(instance=client_progress,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=client_progress,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(CLIENT_PROGRESS_DETAILS),
                              "data": serializer.data})

    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        client_progress = self.get_object()

        client_progress_id = self.kwargs.get("client_progress_id")
        serializer = self.serializer_class(
                            instance=client_progress,
                            data=request.data,
                            partial=True,
                            context={"client_progress_id": client_progress_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(CLIENT_PROGRESS_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(CLIENT_PROGRESS_NOT_UPDATED_MSG),
                              "data": serializer.errors})

    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        client_progress = self.get_object()

        client_progress_id = self.kwargs.get("client_progress_id")
        serializer = self.serializer_class(
                            instance=client_progress,
                            data=request.data,
                            partial=True,
                            context={"client_progress_id": client_progress_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(CLIENT_PROGRESS_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(CLIENT_PROGRESS_NOT_UPDATED_MSG),
                              "data": serializer.errors})


class GroupClientProgressByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = GroupClientProgressRetrieveUpdateDeleteModelSerializer

    def get_object(self):
        client_progress_id = self.kwargs.get("client_progress_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        client_progress_object = get_object_or_404(GroupClientProgress,
                                                   id=client_progress_id)  # As one dictionary object, with exception

        # client_progress_object = GroupClientProgress.objects.filter(id=client_progress_id).first()  # As one dictionary object, exception should be handled
        # client_progress_object = GroupClientProgress.objects.filter(id=client_progress_id)  # As list with a dictionary element, exception should be handled
        #
        # if not client_progress_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_CLIENT_PROGRESS_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return client_progress_object

    def get(self, request, *args, **kwargs):
        client_progress = self.get_object()

        serializer = self.serializer_class(instance=client_progress,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=client_progress,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(CLIENT_PROGRESS_DETAILS),
                              "data": serializer.data})

    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)})

        client_progress = self.get_object()
        client_progress.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(CLIENT_PROGRESS_DELETED_MSG),
                              "data": {}
                              })
