# Create your views here.

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_ADMINISTRATORS_MSG,
                                                    ALL_ADMINISTRATORS_MSG,
                                                    ADMINISTRATOR_CREATED_MSG,
                                                    ADMINISTRATOR_NOT_CREATED_MSG,
                                                    NO_ADMINISTRATOR_WITH_ID_MSG,
                                                    ADMINISTRATOR_DETAILS,
                                                    ADMINISTRATOR_UPDATED_MSG,
                                                    ADMINISTRATOR_NOT_UPDATED_MSG,
                                                    ADMINISTRATOR_DELETED_MSG
                                                    )

from apps.api.messages_api.messages_errors import (NOT_SUPERUSER_FORBIDDEN,
                                                   DELETE_YOURSELF_FORBIDDEN,
                                                   INACTIVE_YOURSELF_FORBIDDEN,
                                                   )

from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveDestroyAPIView,
                                     )

from apps.api.administrator.serializers import (AdministratorAllFieldsModelSerializer,
                                         AdministratorCreateModelSerializer,
                                         AdministratorRetrieveUpdateDeleteModelSerializer,
                                         )

from apps.api.administrator.models import Administrator
from apps.api.user.models import User



class AllAdministratorsGenericList(ListAPIView):
    serializer_class = AdministratorAllFieldsModelSerializer

    def get_queryset(self):
        administrators = Administrator.objects.filter()  # Staff can see all users except superusers
        return administrators

    def get(self, request: Request, *args, **kwargs):
        administrators = self.get_queryset()

        if not administrators:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_ADMINISTRATORS_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=administrators, many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_ADMINISTRATORS_MSG),
                              "data": serializer.data}
                        )



class CreateNewAdministratorGenericCreate(CreateAPIView):
    serializer_class = AdministratorCreateModelSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request":self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(ADMINISTRATOR_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(ADMINISTRATOR_NOT_CREATED_MSG),
                              "data": serializer.errors})



class AdministratorByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = AdministratorRetrieveUpdateDeleteModelSerializer

    def get_object(self, *args, **kwargs):
        administrator_id = self.kwargs.get("administrator_id") # Administrator id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        administrator_object = get_object_or_404(Administrator, id=administrator_id)  # As one dictionary object, with exception

        # administrator_object = Administrator.objects.filter(id=administrator_id).first()  # As one dictionary object, exception should be handled
        # administrator_id_object = Administrator.objects.filter(id=administrator_id)  # As list with a dictionary element, exception should be handled
        #
        # if not administrator_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_ADMINISTRATOR_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return administrator_object


    def get(self, request, *args, **kwargs):
        administrator = self.get_object()

        serializer=self.serializer_class(instance=administrator,  # If one dictionary object, got with get_or_404()
                                         context={"request":self.request})
        # serializer=self.serializer_class(instance=administrator,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message":gettext_lazy(ADMINISTRATOR_DETAILS),
                              "data": serializer.data} )


    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        administrator = self.get_object()

        administrator_id = self.kwargs.get("administrator_id")
        serializer = self.serializer_class(instance=administrator,
                                           data=request.data,
                                           partial=True,
                                           context={"administrator_id": administrator_id,  # Additionally transferred for serializer validation
                                                    "request":self.request,
                                                    }
                                           )

        if serializer.is_valid():
            serializer.save()

            user_is_active = serializer.validated_data.get("user_is_active")
            administrator_user_id = Administrator.objects.get(id=administrator_id).user.id
            administrator_user = User.objects.filter(id=administrator_user_id)
            if administrator_user.first().is_active != user_is_active:
                administrator_user.update(is_active=user_is_active)

            serializer = self.serializer_class(instance=administrator,
                                               data=request.data,
                                               partial=True,
                                               context={"administrator_id": administrator_id,
                                                        "request": self.request,
                                                        }
                                               )
            if serializer.is_valid():
                serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message":gettext_lazy(ADMINISTRATOR_UPDATED_MSG),
                                  "data":serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message":gettext_lazy(ADMINISTRATOR_NOT_UPDATED_MSG),
                              "data": serializer.errors})


    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        administrator = self.get_object()


        administrator_id = self.kwargs.get("administrator_id")

        serializer = self.serializer_class(instance=administrator,
                                           data=request.data,
                                           partial=True,
                                           context={"administrator_id": administrator_id,  # Add transferred for serializer validation
                                                    "request":self.request,
                                                    }
                                           )

        if serializer.is_valid():
            serializer.save()

            user_is_active = serializer.validated_data.get("user_is_active")
            administrator_user_id = Administrator.objects.get(id=administrator_id).user.id
            administrator_user = User.objects.filter(id=administrator_user_id)
            if administrator_user.first().is_active != user_is_active:
                administrator_user.update(is_active=user_is_active)

            serializer = self.serializer_class(instance=administrator,
                                               data=request.data,
                                               partial=True,
                                               context={"administrator_id": administrator_id,
                                                        "request": self.request,
                                                        }
                                               )
            if serializer.is_valid():
                serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message":gettext_lazy(ADMINISTRATOR_UPDATED_MSG),
                                  "data":serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message":gettext_lazy(ADMINISTRATOR_NOT_UPDATED_MSG),
                              "data": serializer.errors})



class AdministratorByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = AdministratorRetrieveUpdateDeleteModelSerializer

    def get_object(self):
        administrator_id = self.kwargs.get("administrator_id") # Administrator id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        administrator_object = get_object_or_404(Administrator, id=administrator_id)  # As one dictionary object, with exception

        # administrator_object = Administrator.objects.filter(id=administrator_id).first()  # As one dictionary object, exception should be handled
        # administrator_id_object = Administrator.objects.filter(id=administrator_id)  # As list with a dictionary element, exception should be handled
        #
        # if not administrator_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_ADMINISTRATOR_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return administrator_object


    def get(self, request, *args, **kwargs):
        administrator = self.get_object()

        serializer = self.serializer_class(instance=administrator,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=administrator,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ADMINISTRATOR_DETAILS),
                              "data": serializer.data})


    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_FORBIDDEN)})

        administrator = self.get_object()
        administrator.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ADMINISTRATOR_DELETED_MSG),
                              "data": {}
                              })
