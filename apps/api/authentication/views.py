from django.shortcuts import (render,
                              redirect,
                              )

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from django.utils.translation import gettext_lazy
from apps.api.messages_api.messages_actions import LOG_OUT_SUCCESS

from django.contrib import auth


def logout_function(request: Request):
    auth.logout(request)
    return redirect("router:jwt_auth:jwt-obtain-token")  # Change to another url, if necessary
