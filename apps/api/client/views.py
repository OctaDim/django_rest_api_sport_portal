# Create your views here.

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_CLIENTS_MSG,
                                                    ALL_CLIENTS_MSG,
                                                    CLIENT_CREATED_MSG,
                                                    CLIENT_NOT_CREATED_MSG,
                                                    NO_CLIENT_WITH_ID_MSG,
                                                    CLIENT_DETAILS,
                                                    CLIENT_UPDATED_MSG,
                                                    CLIENT_NOT_UPDATED_MSG,
                                                    CLIENT_DELETED_MSG
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

from apps.api.client.serializers import (ClientAllFieldsModelSerializer,
                                         ClientCreateModelSerializer,
                                         ClientRetrieveUpdateDeleteModelSerializer,
                                         )

from apps.api.client.models import Client
from apps.api.user.models import User



class AllClientsGenericList(ListAPIView):
    serializer_class = ClientAllFieldsModelSerializer

    def get_queryset(self):
        clients = Client.objects.filter()  # Staff can see all users except superusers
        return clients

    def get(self, request: Request, *args, **kwargs):
        clients = self.get_queryset()

        if not clients:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_CLIENTS_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=clients, many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_CLIENTS_MSG),
                              "data": serializer.data}
                        )



class CreateNewClientGenericCreate(CreateAPIView):
    serializer_class = ClientCreateModelSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request":self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(CLIENT_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(CLIENT_NOT_CREATED_MSG),
                              "data": serializer.errors})



class ClientByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = ClientRetrieveUpdateDeleteModelSerializer

    def get_object(self, *args, **kwargs):
        client_id = self.kwargs.get("client_id") # Client id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        client_object = get_object_or_404(Client, id=client_id)  # As one dictionary object, with exception

        # client_object = Client.objects.filter(id=client_id).first()  # As one dictionary object, exception should be handled
        # client_id_object = Client.objects.filter(id=client_id)  # As list with a dictionary element, exception should be handled
        #
        # if not client_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_CLIENT_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return client_object


    def get(self, request, *args, **kwargs):
        client = self.get_object()

        serializer=self.serializer_class(instance=client,  # If one dictionary object, got with get_or_404()
                                         context={"request":self.request})
        # serializer=self.serializer_class(instance=client,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message":gettext_lazy(CLIENT_DETAILS),
                              "data": serializer.data} )


    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        client = self.get_object()

        client_id = self.kwargs.get("client_id")
        serializer = self.serializer_class(instance=client,
                                           data=request.data,
                                           partial=True,
                                           context={"client_id": client_id,  # Additionally transferred for serializer validation
                                                    "request":self.request,
                                                    }
                                           )

        if serializer.is_valid():
            serializer.save()

            user_is_active = serializer.validated_data.get("user_is_active")
            client_user_id = Client.objects.get(id=client_id).user.id
            client_user = User.objects.filter(id=client_user_id)
            if client_user.first().is_active != user_is_active:
                client_user.update(is_active=user_is_active)

            serializer = self.serializer_class(instance=client,
                                               data=request.data,
                                               partial=True,
                                               context={"client_id": client_id,
                                                        "request": self.request,
                                                        }
                                               )
            if serializer.is_valid():
                serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message":gettext_lazy(CLIENT_UPDATED_MSG),
                                  "data":serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message":gettext_lazy(CLIENT_NOT_UPDATED_MSG),
                              "data": serializer.errors})


    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        client = self.get_object()


        client_id = self.kwargs.get("client_id")

        serializer = self.serializer_class(instance=client,
                                           data=request.data,
                                           partial=True,
                                           context={"client_id": client_id,  # Add transferred for serializer validation
                                                    "request":self.request,
                                                    }
                                           )

        if serializer.is_valid():
            serializer.save()

            user_is_active = serializer.validated_data.get("user_is_active")
            client_user_id = Client.objects.get(id=client_id).user.id
            client_user = User.objects.filter(id=client_user_id)
            if client_user.first().is_active != user_is_active:
                client_user.update(is_active=user_is_active)

            serializer = self.serializer_class(instance=client,
                                               data=request.data,
                                               partial=True,
                                               context={"client_id": client_id,
                                                        "request": self.request,
                                                        }
                                               )
            if serializer.is_valid():
                serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message":gettext_lazy(CLIENT_UPDATED_MSG),
                                  "data":serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message":gettext_lazy(CLIENT_NOT_UPDATED_MSG),
                              "data": serializer.errors})



class ClientByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = ClientRetrieveUpdateDeleteModelSerializer

    def get_object(self):
        client_id = self.kwargs.get("client_id") # Client id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        client_object = get_object_or_404(Client, id=client_id)  # As one dictionary object, with exception

        # client_object = Client.objects.filter(id=client_id).first()  # As one dictionary object, exception should be handled
        # client_id_object = Client.objects.filter(id=client_id)  # As list with a dictionary element, exception should be handled
        #
        # if not client_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_CLIENT_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return client_object


    def get(self, request, *args, **kwargs):
        client = self.get_object()

        serializer = self.serializer_class(instance=client,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=client,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(CLIENT_DETAILS),
                              "data": serializer.data})


    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)})

        client = self.get_object()
        client.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(CLIENT_DELETED_MSG),
                              "data": {}
                              })
