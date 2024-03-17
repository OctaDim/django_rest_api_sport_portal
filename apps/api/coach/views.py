# Create your views here.

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_COACHES_MSG,
                                                    ALL_COACHES_MSG,
                                                    COACH_CREATED_MSG,
                                                    COACH_NOT_CREATED_MSG,
                                                    NO_COACH_WITH_ID_MSG,
                                                    COACH_DETAILS,
                                                    COACH_UPDATED_MSG,
                                                    COACH_NOT_UPDATED_MSG,
                                                    COACH_DELETED_MSG
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

from apps.api.coach.serializers import (CoachAllFieldsModelSerializer,
                                         CoachCreateModelSerializer,
                                         CoachRetrieveUpdateDeleteModelSerializer,
                                         )

from apps.api.coach.models import Coach
from apps.api.user.models import User



class AllCoachesGenericList(ListAPIView):
    serializer_class = CoachAllFieldsModelSerializer

    def get_queryset(self):
        coaches = Coach.objects.filter()  # Staff can see all users except superusers
        return coaches

    def get(self, request: Request, *args, **kwargs):
        coaches = self.get_queryset()

        if not coaches:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_COACHES_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=coaches, many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_COACHES_MSG),
                              "data": serializer.data}
                        )



class CreateNewCoachGenericCreate(CreateAPIView):
    serializer_class = CoachCreateModelSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request":self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(COACH_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(COACH_NOT_CREATED_MSG),
                              "data": serializer.errors})



class CoachByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = CoachRetrieveUpdateDeleteModelSerializer

    def get_object(self, *args, **kwargs):
        coach_id = self.kwargs.get("coach_id") # Coach id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        coach_object = get_object_or_404(Coach, id=coach_id)  # As one dictionary object, with exception

        # coach_object = Coach.objects.filter(id=coach_id).first()  # As one dictionary object, exception should be handled
        # coach_id_object = Coach.objects.filter(id=coach_id)  # As list with a dictionary element, exception should be handled
        #
        # if not coach_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_COACH_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return coach_object


    def get(self, request, *args, **kwargs):
        coach = self.get_object()

        serializer=self.serializer_class(instance=coach,  # If one dictionary object, got with get_or_404()
                                         context={"request":self.request})
        # serializer=self.serializer_class(instance=coach,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message":gettext_lazy(COACH_DETAILS),
                              "data": serializer.data} )


    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        coach = self.get_object()

        coach_id = self.kwargs.get("coach_id")
        serializer = self.serializer_class(instance=coach,
                                           data=request.data,
                                           partial=True,
                                           context={"coach_id": coach_id,  # Additionally transferred for serializer validation
                                                    "request":self.request,
                                                    }
                                           )

        if serializer.is_valid():
            serializer.save()

            user_is_active = serializer.validated_data.get("user_is_active")
            coach_user_id = Coach.objects.get(id=coach_id).user.id
            coach_user = User.objects.filter(id=coach_user_id)
            if coach_user.first().is_active != user_is_active:
                coach_user.update(is_active=user_is_active)

            serializer = self.serializer_class(instance=coach,
                                               data=request.data,
                                               partial=True,
                                               context={"coach_id": coach_id,
                                                        "request": self.request,
                                                        }
                                               )
            if serializer.is_valid():
                serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message":gettext_lazy(COACH_UPDATED_MSG),
                                  "data":serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message":gettext_lazy(COACH_NOT_UPDATED_MSG),
                              "data": serializer.errors})


    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        coach = self.get_object()


        coach_id = self.kwargs.get("coach_id")

        serializer = self.serializer_class(instance=coach,
                                           data=request.data,
                                           partial=True,
                                           context={"coach_id": coach_id,  # Add transferred for serializer validation
                                                    "request":self.request,
                                                    }
                                           )

        if serializer.is_valid():
            serializer.save()

            user_is_active = serializer.validated_data.get("user_is_active")
            coach_user_id = Coach.objects.get(id=coach_id).user.id
            coach_user = User.objects.filter(id=coach_user_id)
            if coach_user.first().is_active != user_is_active:
                coach_user.update(is_active=user_is_active)

            serializer = self.serializer_class(instance=coach,
                                               data=request.data,
                                               partial=True,
                                               context={"coach_id": coach_id,
                                                        "request": self.request,
                                                        }
                                               )
            if serializer.is_valid():
                serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message":gettext_lazy(COACH_UPDATED_MSG),
                                  "data":serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message":gettext_lazy(COACH_NOT_UPDATED_MSG),
                              "data": serializer.errors})



class CoachByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = CoachRetrieveUpdateDeleteModelSerializer

    def get_object(self):
        coach_id = self.kwargs.get("coach_id") # Coach id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        coach_object = get_object_or_404(Coach, id=coach_id)  # As one dictionary object, with exception

        # coach_object = Coach.objects.filter(id=coach_id).first()  # As one dictionary object, exception should be handled
        # coach_id_object = Coach.objects.filter(id=coach_id)  # As list with a dictionary element, exception should be handled
        #
        # if not coach_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_COACH_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return coach_object


    def get(self, request, *args, **kwargs):
        coach = self.get_object()

        serializer = self.serializer_class(instance=coach,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=coach,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(COACH_DETAILS),
                              "data": serializer.data})


    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)})

        coach = self.get_object()
        coach.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(COACH_DELETED_MSG),
                              "data": {}
                              })
