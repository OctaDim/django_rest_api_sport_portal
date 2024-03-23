from django.shortcuts import (render,
                              redirect)

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from django.utils.translation import gettext_lazy

from django.contrib import auth

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.exceptions import (TokenError,
                                                 InvalidToken)

from apps.api.authentication_jwt.serializers import CustomTokenObtainPairSerializer

from apps.api.messages_api.messages_actions import LOG_IN_SUCCESS, LOG_OUT_SUCCESS


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as error:
            raise InvalidToken(error.args[0])

        access_token = serializer.validated_data["access"]
        refresh_token = serializer.validated_data["refresh"]

        return Response(status=status.HTTP_200_OK,
                        data = {"message": gettext_lazy(LOG_IN_SUCCESS),
                                "validated_data": serializer.validated_data,
                                "access_token": access_token,
                                "refresh_token": refresh_token}
                        )


def logout_function(request: Request):
    auth.logout(request)
    return redirect("router:jwt_auth:jwt-obtain-token")
