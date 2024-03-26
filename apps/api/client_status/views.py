# Create your views here.

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_CLIENT_STATUSES_MSG,
                                                    ALL_CLIENT_STATUSES_MSG,
                                                    CLIENT_STATUS_CREATED_MSG,
                                                    CLIENT_STATUS_NOT_CREATED_MSG,
                                                    NO_CLIENT_STATUS_WITH_ID_MSG,
                                                    CLIENT_STATUS_DETAILS,
                                                    CLIENT_STATUS_UPDATED_MSG,
                                                    CLIENT_STATUS_NOT_UPDATED_MSG,
                                                    CLIENT_STATUS_DELETED_MSG
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

from apps.api.client_status.serializers import (
                        ClientStatusAllFieldsModelSerializer,
                        ClientStatusCreateModelSerializer,
                        ClientStatusRetrieveUpdateDeleteModelSerializer)

from apps.api.client_status.models import ClientStatus

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from apps.api.authentication.permissions_custom import (IsSuperuser,
                                                        IsAdministrator,
                                                        IsCoach,
                                                        IsClient,
                                                        IsActive,
                                                        IsVerified)


class AllClientStatusesGenericList(ListAPIView):
    serializer_class = ClientStatusAllFieldsModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_queryset(self):
        client_statuses = ClientStatus.objects.filter()
        return client_statuses

    def get(self, request: Request, *args, **kwargs):
        client_statuses = self.get_queryset()

        if not client_statuses:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_CLIENT_STATUSES_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=client_statuses,
                                           many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_CLIENT_STATUSES_MSG),
                              "data": serializer.data}
                        )



class CreateNewClientStatusGenericCreate(CreateAPIView):
    serializer_class = ClientStatusCreateModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(CLIENT_STATUS_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(CLIENT_STATUS_NOT_CREATED_MSG),
                              "data": serializer.errors})



class ClientStatusByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = ClientStatusRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self, *args, **kwargs):
        client_status_id = self.kwargs.get("client_status_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        client_status_object = get_object_or_404(ClientStatus,
                                                 id=client_status_id)  # As one dictionary object, with exception

        # client_status_object = ClientStatus.objects.filter(id=client_status_id).first()  # As one dictionary object, exception should be handled
        # client_status_object = ClientStatus.objects.filter(id=client_status_id)  # As list with a dictionary element, exception should be handled
        #
        # if not client_status_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_CLIENT_STATUS_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return client_status_object

    def get(self, request, *args, **kwargs):
        client_status = self.get_object()

        serializer = self.serializer_class(instance=client_status,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=client_status,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(CLIENT_STATUS_DETAILS),
                              "data": serializer.data})

    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        client_status = self.get_object()

        client_status_id = self.kwargs.get("client_status_id")
        serializer = self.serializer_class(
                            instance=client_status,
                            data=request.data,
                            partial=True,
                            context={"client_status_id": client_status_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(CLIENT_STATUS_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(CLIENT_STATUS_NOT_UPDATED_MSG),
                              "data": serializer.errors})

    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        client_status = self.get_object()

        client_status_id = self.kwargs.get("client_status_id")
        serializer = self.serializer_class(
                            instance=client_status,
                            data=request.data,
                            partial=True,
                            context={"client_status_id": client_status_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(CLIENT_STATUS_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(CLIENT_STATUS_NOT_UPDATED_MSG),
                              "data": serializer.errors})

class ClientStatusByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = ClientStatusRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self):
        client_status_id = self.kwargs.get("client_status_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        client_status_object = get_object_or_404(ClientStatus,
                                                 id=client_status_id)  # As one dictionary object, with exception

        # client_status_object = ClientStatus.objects.filter(id=client_status_id).first()  # As one dictionary object, exception should be handled
        # client_status_object = ClientStatus.objects.filter(id=client_status_id)  # As list with a dictionary element, exception should be handled
        #
        # if not client_status_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_CLIENT_STATUS_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return client_status_object

    def get(self, request, *args, **kwargs):
        client_status = self.get_object()

        serializer = self.serializer_class(instance=client_status,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=client_status,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(CLIENT_STATUS_DETAILS),
                              "data": serializer.data})

    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)})

        client_status = self.get_object()
        client_status.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(CLIENT_STATUS_DELETED_MSG),
                              "data": {}
                              })
