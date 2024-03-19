# Create your views here.

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_DEPARTMENTS_MSG,
                                                    ALL_DEPARTMENTS_MSG,
                                                    DEPARTMENT_CREATED_MSG,
                                                    DEPARTMENT_NOT_CREATED_MSG,
                                                    NO_DEPARTMENT_WITH_ID_MSG,
                                                    DEPARTMENT_DETAILS,
                                                    DEPARTMENT_UPDATED_MSG,
                                                    DEPARTMENT_NOT_UPDATED_MSG,
                                                    DEPARTMENT_DELETED_MSG
                                                    )

from apps.api.messages_api.messages_errors import (NOT_SUPERUSER_HARD_DELETE_FORBIDDEN,
                                                   NOT_SUPERUSER_FORBIDDEN,
                                                   DELETE_YOURSELF_FORBIDDEN,
                                                   INACTIVE_YOURSELF_FORBIDDEN,
                                                   )

from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveDestroyAPIView,
                                     )

from apps.api.department.serializers import (
    DepartmentAllFieldsModelSerializer,
    DepartmentCreateModelSerializer,
    DepartmentRetrieveUpdateDeleteModelSerializer,
)

from apps.api.department.models import Department
from apps.api.user.models import User



class AllDepartmentsGenericList(ListAPIView):
    serializer_class = DepartmentAllFieldsModelSerializer

    def get_queryset(self):
        departments = Department.objects.filter()
        return departments

    def get(self, request: Request, *args, **kwargs):
        departments = self.get_queryset()

        if not departments:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_DEPARTMENTS_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=departments, many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_DEPARTMENTS_MSG),
                              "data": serializer.data}
                        )



class CreateNewDepartmentGenericCreate(CreateAPIView):
    serializer_class = DepartmentCreateModelSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(DEPARTMENT_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(DEPARTMENT_NOT_CREATED_MSG),
                              "data": serializer.errors})



class DepartmentByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = DepartmentRetrieveUpdateDeleteModelSerializer

    def get_object(self, *args, **kwargs):
        department_id = self.kwargs.get("department_id")  # Department id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        department_object = get_object_or_404(Department, id=department_id)  # As one dictionary object, with exception

        # department_object = Department.objects.filter(id=department_id).first()  # As one dictionary object, exception should be handled
        # department_id_object = Department.objects.filter(id=department_id)  # As list with a dictionary element, exception should be handled
        #
        # if not department_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_DEPARTMENT_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return department_object

    def get(self, request, *args, **kwargs):
        department = self.get_object()

        serializer = self.serializer_class(instance=department,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=department,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(DEPARTMENT_DETAILS),
                              "data": serializer.data})

    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        department = self.get_object()

        department_id = self.kwargs.get("department_id")
        serializer = self.serializer_class(instance=department,
                                           data=request.data,
                                           partial=True,
                                           context={"department_id": department_id,
                                                    # Additionally transferred for serializer validation
                                                    "request": self.request,
                                                    }
                                           )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(DEPARTMENT_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(DEPARTMENT_NOT_UPDATED_MSG),
                              "data": serializer.errors})

    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        department = self.get_object()

        department_id = self.kwargs.get("department_id")

        serializer = self.serializer_class(instance=department,
                                           data=request.data,
                                           partial=True,
                                           context={"department_id": department_id,  # Add transferred for serializer validation
                                                    "request": self.request,
                                                    }
                                           )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(DEPARTMENT_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(DEPARTMENT_NOT_UPDATED_MSG),
                              "data": serializer.errors})



class DepartmentByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = DepartmentRetrieveUpdateDeleteModelSerializer

    def get_object(self):
        department_id = self.kwargs.get("department_id")  # Department id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        department_object = get_object_or_404(Department, id=department_id)  # As one dictionary object, with exception

        # department_object = Department.objects.filter(id=department_id).first()  # As one dictionary object, exception should be handled
        # department_id_object = Department.objects.filter(id=department_id)  # As list with a dictionary element, exception should be handled
        #
        # if not department_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_DEPARTMENT_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return department_object

    def get(self, request, *args, **kwargs):
        department = self.get_object()

        serializer = self.serializer_class(instance=department,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=department,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(DEPARTMENT_DETAILS),
                              "data": serializer.data})

    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)})

        department = self.get_object()
        department.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(DEPARTMENT_DELETED_MSG),
                              "data": {}
                              })
