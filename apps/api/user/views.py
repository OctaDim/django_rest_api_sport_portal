from django.shortcuts import render
# Create your views here.

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from apps.api.user.serializers import AllUsersModelSerializer

from rest_framework.generics import ListAPIView

from django.contrib.auth.models import User


class ListAllUsersGenericList(ListAPIView):
    serializer_class = AllUsersModelSerializer

    def get_queryset(self):
        users = User.objects.all()
        return users

    def get(self, request: Request, *args, **kwargs):
        users = self.get_queryset()

        if not users:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": "No user exists",
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=users)
        return Response(status=status.HTTP_200_OK,
                        data={"message": "All users list",
                              "data": serializer.data}
                        )
