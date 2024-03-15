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
                                                    CLIENT_DETAILS,
                                                    CLIENT_UPDATED_MSG,
                                                    CLIENT_NOT_UPDATED_MSG,
                                                    CLIENT_DELETED_MSG
                                                    )

from apps.api.messages_api.messages_errors import (NOT_SUPERUSER_FORBIDDEN,
                                                   DELETE_YOURSELF_FORBIDDEN,
                                                   INACTIVE_YOURSELF_FORBIDDEN,
                                                   )

from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveUpdateAPIView,
                                     )

from apps.api.client.serializers import (ClientAllFieldsModelSerializer,
                                         ClientCreateModelSerializer,
                                         )

from apps.api.client.models import Client



class AllClientsGenericList(ListAPIView):
    serializer_class = ClientAllFieldsModelSerializer

    def get_queryset(self):
        queryset = Client.objects.filter()  # Staff can see all users except superusers
        return queryset

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
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # serializer.validated_data["client_creator"]
            serializer.save()
            # serializer.save(commit=False)
            # serializer["client_creator"] = self.request.user
            # serializer.save
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(CLIENT_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(CLIENT_NOT_CREATED_MSG),
                              "data": serializer.errors})
