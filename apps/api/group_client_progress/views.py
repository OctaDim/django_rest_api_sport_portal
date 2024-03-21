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
)

from apps.api.group_client_progress.models import GroupClientProgress
from apps.api.user.models import User



class AllClientsProgressGenericList(ListAPIView):
    serializer_class = GroupClientProgressAllFieldsModelSerializer

    def get_queryset(self):
        clients_progress = GroupClientProgress.objects.filter()
        return clients_progress

    def get(self, request: Request, *args, **kwargs):
        clients_progress = self.get_queryset()

        if not clients_progress:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_CLIENTS_PROGRESS_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=clients_progress, many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_CLIENTS_PROGRESS_MSG),
                              "data": serializer.data}
                        )



class CreateNewClientProgressGenericCreate(CreateAPIView):
    pass



class ClientProgressByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    pass



class ClientProgressByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    pass
