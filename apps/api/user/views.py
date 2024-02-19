from django.shortcuts import render
# Create your views here.

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
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
                               STAFF_USER_CREATED_MSG,
                               STAFF_USER_NOT_CREATED_MSG,
                               TRAINER_USER_CREATED_MSG,
                               TRAINER_USER_NOT_CREATED_MSG,
                               USER_DETAILS, USER_UPDATED_MSG,
                               USER_NOT_UPDATED_MSG,
                               USER_DELETED_MSG
                               )

from apps.api.messages_errors import (NOT_SUPERUSER_FORBIDDEN,
                                      NOT_STAFF_USER_FORBIDDEN,
                                      )

# ##################### TRIAL CODE #####################################
from apps.api.user.serializers_test_any_user_reg import (
                                    _Test_UserRegistrySerializer,
                                    _Test_SuperUserRegistrySerializer,
                                    _Test_StaffUserRegistrySerializer,
                                    _Test_TrainerUserRegistrySerializer)
# ######################################################################

from apps.api.user.serializer_user_reg import UserRegistrySerializer
from apps.api.user.serializer_superuser_reg import SuperUserRegistrySerializer
from apps.api.user.serializer_staff_user_reg import StaffUserRegistrySerializer
from apps.api.user.serializer_trainer_user_reg import TrainerUserRegistrySerializer

from apps.api.user.serializers import (AllUsersSerializer,
                                       UserInfoByIdAllFieldsSerializer,
                                       )

from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     )



class AllUsersGenericListForSuperuser(ListAPIView):
    serializer_class = UsersSerializerAllFields

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

        # user_is_staff = request.user.is_staff  # Commented, because will be defined by Permissions classes
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


class RegisterNewTrainerUserGenericCreate(CreateAPIView):
    serializer_class = TrainerUserRegistrySerializer

    def post(self, request, *args, **kwargs):

        # user_is_staff = request.user.is_staff  # Commented, because will be defined by Permissions classes
        # if not user_is_staff:
        #     return Response(
        #         status=status.HTTP_403_FORBIDDEN,
        #         data={"message":gettext_lazy(NOT_STAFF_USER_FORBIDDEN)})

        cerializer = self.serializer_class(data=request.data)
        if cerializer.is_valid():
            cerializer.save()
            return Response(
                    status=status.HTTP_200_OK,
                    data={"message":gettext_lazy(TRAINER_USER_CREATED_MSG),
                          "data":cerializer.data})

        return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message":gettext_lazy(TRAINER_USER_NOT_CREATED_MSG),
                      "data":cerializer.errors})



# ######################################################################
# ########################## TRIAL CODE ################################
# ######################################################################

class _Test_RegisterNewUserGenericCreate(CreateAPIView):
    serializer_class = _Test_UserRegistrySerializer

    def post(self, request: Request, *args, **kwargs):
        # req_data = dict(request.data)  # Option 3: Not recommended, better in serializer. Not for custom manager
        # req_data_dict = {fld: val[0] for fld, val in req_data.items() if val[0] != ""}
        # _Test_UserRegistrySerializer.Meta.fields.append("is_staff")
        # _Test_UserRegistrySerializer.Meta.fields.append("is_superuser")
        # req_data_dict["is_staff"] = "False"
        # req_data_dict["is_superuser"] = "False"
        # serializer = self.serializer_class(data=req_data_dict)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message":gettext_lazy(USER_CREATED_MSG),
                                  "data":serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message":gettext_lazy(USER_NOT_CREATED_MSG),
                              "data":serializer.errors})


class _Test_RegisterNewSuperUserGenericCreate(CreateAPIView):
    serializer_class = _Test_SuperUserRegistrySerializer

    def post(self, request: Request, *args, **kwargs):

        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_FORBIDDEN)})

        # req_data = dict(request.data)  # Option 3: Not recommended, better in serializer. Not for custom manager
        # req_data_dict = {fld: val[0] for fld, val in req_data.items() if val[0] != ""}
        # _Test_SuperUserRegistrySerializer.Meta.fields.append("is_staff")
        # _Test_SuperUserRegistrySerializer.Meta.fields.append("is_superuser")
        # req_data_dict["is_staff"] = "True"
        # req_data_dict["is_superuser"] = "True"
        # serializer = self.serializer_class(data=req_data_dict)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message":gettext_lazy(SUPERUSER_CREATED_MSG),
                                  "data":serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message":gettext_lazy(SUPERUSER_NOT_CREATED_MSG),
                              "data":serializer.errors})


class _Test_RegisterNewStaffUserGenericCreate(CreateAPIView):
    serializer_class = _Test_StaffUserRegistrySerializer

    def post(self, request: Request, *args, **kwargs):
        # req_data = dict(request.data)  # Option 3: Not recommended, better in serializer. Not for custom manager
        # req_data_dict = {fld: val[0] for fld, val in req_data.items() if val[0] != ""}
        # _Test_StaffUserRegistrySerializer.Meta.fields.append("is_staff")
        # _Test_StaffUserRegistrySerializer.Meta.fields.append("is_superuser")
        # req_data_dict["is_staff"] = "True"
        # req_data_dict["is_superuser"] = "False"
        # serializer = self.serializer_class(data=req_data_dict)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message":gettext_lazy(STAFF_USER_CREATED_MSG),
                                  "data":serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message":gettext_lazy(STAFF_USER_NOT_CREATED_MSG),
                              "data":serializer.errors})


class _Test_RegisterNewTrainerUserGenericCreate(CreateAPIView):
    serializer_class = _Test_TrainerUserRegistrySerializer

    def post(self, request: Request, *args, **kwargs):
        # req_data = dict(request.data)  # Option 3: Not recommended, better in serializer. Not for custom manager
        # req_data_dict = {fld: val[0] for fld, val in req_data.items() if val[0] != ""}
        # _Test_StaffUserRegistrySerializer.Meta.fields.append("is_staff")
        # _Test_StaffUserRegistrySerializer.Meta.fields.append("is_superuser")
        # req_data_dict["is_staff"] = "True"
        # req_data_dict["is_superuser"] = "False"
        # serializer = self.serializer_class(data=req_data_dict)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message":gettext_lazy(TRAINER_USER_CREATED_MSG),
                                  "data":serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message":gettext_lazy(TRAINER_USER_NOT_CREATED_MSG),
                              "data":serializer.errors})

# ######################################################################
# ######################################################################
# ######################################################################


class UserInfoByIdGenericRetrieveUpdDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = UserInfoByIdAllFieldsSerializer

    def get_object(self):

        user_id = self.kwargs.get("user_id")  # User id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        user_object = get_object_or_404(User, id=user_id)  # As one dictionary object, with exception
        # user_object = User.objects.filter(id=user_id).first()  # As one dictionary object, exception should be handled
        # user_object = User.objects.filter(id=user_id)  # As list with a dictionary element, exception should be handled

        return user_object


    def get(self, request, *args, **kwargs):

        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_FORBIDDEN)})

        user = self.get_object()

        serializer=self.serializer_class(instance=user)  # If one dictionary object, got with get_or_404()
        # serializer=self.serializer_class(instance=user, many=True)  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message":gettext_lazy(USER_DETAILS),
                              "data": serializer.data} )


    def patch(self, request, *args, **kwargs):

        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_FORBIDDEN)})

        user = self.get_object()

        serializer = self.serializer_class(instance=user,
                                           data=request.data,
                                           partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message":gettext_lazy(USER_UPDATED_MSG),
                                  "data":serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message":gettext_lazy(USER_NOT_UPDATED_MSG),
                              "data": serializer.errors})


    # def patch(self, request, *args, **kwargs):
    #     user = self.get_object()
    #
    #     serializer = self.serializer_class(instance=user,
    #                                        data=request.data,
    #                                        partial=True)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(status=status.HTTP_200_OK,
    #                         data={"message":gettext_lazy(USER_UPDATED_MSG),
    #                               "data":serializer.data})
    #
    #     return Response(status=status.HTTP_400_BAD_REQUEST,
    #                     data={"message":gettext_lazy(USER_NOT_UPDATED_MSG),
    #                           "data": serializer.errors})


    def delete(self, request, *args, **kwargs):

        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_FORBIDDEN)})

        user = self.get_object()

        user.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message":gettext_lazy(USER_DELETED_MSG),
                              "data": []})
