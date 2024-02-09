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

from apps.api.messages import (USERS_NOT_FOUND,
                               ALL_USERS_LIST,
                               )

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
                            data={"message": gettext_lazy(USERS_NOT_FOUND),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=users, many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_USERS_LIST),
                              "data": serializer.data}
                        )


class RegisterNewUserGenericCreate(CreateAPIView):
    pass
