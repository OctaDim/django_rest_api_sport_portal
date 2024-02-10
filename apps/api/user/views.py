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
                               )

from apps.api.user.serzer_user_reg import UserRegistrySerializer

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
