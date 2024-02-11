from django.shortcuts import render
# Create your views here.

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from django.utils.translation import gettext_lazy

# ##################################################################
# from django.contrib.auth.models import User  # Django default user
from apps.api.user.models import User  # Custom user
# ##################################################################

from apps.api.messages import (NO_USERS_MSG,
                               ALL_USERS_MSG,
                               USER_CREATED_MSG,
                               USER_NOT_CREATED_MSG,
                               SUPERUSER_CREATED_MSG,
                               SUPERUSER_NOT_CREATED_MSG,
                               )

from apps.api.messages_errors import (NOT_SUPERUSER_FORBIDDEN,
                                      NOT_STAFF_USER_FORBIDDEN,
                                      )

from apps.api.user.serzer_user_reg import UserRegistrySerializer
from apps.api.user.serzer_superuser_reg import SuperUserRegistrySerializer
from apps.api.user.serzer_staff_user_reg import StaffUserRegistrySerializer

from apps.api.user.serializers import AllUsersSerializer

from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     )

class ListAllUsersGenericList(ListAPIView):
    serializer_class = AllUsersSerializer

    def get_queryset(self):
        users = User.objects.all()
        return users

    def get(self, request: Request, *args, **kwargs):
        users = self.get_queryset()

        if not users:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": gettext_lazy(NO_USERS_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=users, many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_USERS_MSG),
                              "data": serializer.data}
                        )


class RegisterNewUserGenericCreate(CreateAPIView):
    serializer_class = UserRegistrySerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message":gettext_lazy(USER_CREATED_MSG),
                                  "data":serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message":gettext_lazy(USER_NOT_CREATED_MSG),
                              "data":serializer.errors})


class RegisterNewSuperUserGenericCreate(CreateAPIView):
    serializer_class = SuperUserRegistrySerializer

    def post(self, request, *args, **kwargs):

        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message":gettext_lazy(NOT_SUPERUSER_FORBIDDEN)})

        cerializer = self.serializer_class(data=request.data)
        if cerializer.is_valid():
            cerializer.save()
            return Response(
                    status=status.HTTP_200_OK,
                    data={"message":gettext_lazy(SUPERUSER_CREATED_MSG),
                          "data":cerializer.data})

        return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message":gettext_lazy(SUPERUSER_NOT_CREATED_MSG),
                      "data":cerializer.errors})


class RegisterNewStaffUserGenericCreate(CreateAPIView):
    serializer_class = StaffUserRegistrySerializer

    def post(self, request, *args, **kwargs):

        # user_is_staff = request.user.is_staff  # Commented, because will be defined in Permissions
        # if not user_is_staff:
        #     return Response(
        #         status=status.HTTP_403_FORBIDDEN,
        #         data={"message":gettext_lazy(NOT_STAFF_USER_FORBIDDEN)})

        cerializer = self.serializer_class(data=request.data)
        if cerializer.is_valid():
            cerializer.save()
            return Response(
                    status=status.HTTP_200_OK,
                    data={"message":gettext_lazy(STAFF_USER_CREATED_MSG),
                          "data":cerializer.data})

        return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message":gettext_lazy(STAFF_USER_NOT_CREATED_MSG),
                      "data":cerializer.errors})
