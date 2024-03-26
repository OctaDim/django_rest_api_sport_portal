from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_PAYMENT_TYPES_MSG,
                                                    ALL_PAYMENT_TYPES_MSG,
                                                    PAYMENT_TYPE_CREATED_MSG,
                                                    PAYMENT_TYPE_NOT_CREATED_MSG,
                                                    NO_PAYMENT_TYPE_WITH_ID_MSG,
                                                    PAYMENT_TYPE_DETAILS,
                                                    PAYMENT_TYPE_UPDATED_MSG,
                                                    PAYMENT_TYPE_NOT_UPDATED_MSG,
                                                    PAYMENT_TYPE_DELETED_MSG
                                                    )

from apps.api.messages_api.messages_errors import (
                                    NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)

from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveDestroyAPIView,
                                     )

from apps.api.payment_type.serializers import (
                        PaymentTypeAllFieldsModelSerializer,
                        PaymentTypeCreateModelSerializer,
                        PaymentTypeRetrieveUpdateDeleteModelSerializer)

from apps.api.payment_type.models import PaymentType

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from apps.api.authentication.permissions_custom import (IsSuperuser,
                                                        IsAdministrator,
                                                        IsCoach,
                                                        IsClient,
                                                        IsActive,
                                                        IsVerified)


class AllPaymentTypesGenericList(ListAPIView):
    serializer_class = PaymentTypeAllFieldsModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_queryset(self):
        companies = PaymentType.objects.filter()
        return companies

    def get(self, request: Request, *args, **kwargs):
        companies = self.get_queryset()

        if not companies:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_PAYMENT_TYPES_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=companies,
                                           many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_PAYMENT_TYPES_MSG),
                              "data": serializer.data}
                        )



class CreateNewPaymentTypeGenericCreate(CreateAPIView):
    serializer_class = PaymentTypeCreateModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(PAYMENT_TYPE_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(PAYMENT_TYPE_NOT_CREATED_MSG),
                              "data": serializer.errors})



class PaymentTypeByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = PaymentTypeRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self, *args, **kwargs):
        payment_type_id = self.kwargs.get("payment_type_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        payment_type_object = get_object_or_404(PaymentType,
                                                 id=payment_type_id)  # As one dictionary object, with exception

        # payment_type_object = PaymentType.objects.filter(id=payment_type_id).first()  # As one dictionary object, exception should be handled
        # payment_type_object = PaymentType.objects.filter(id=payment_type_id)  # As list with a dictionary element, exception should be handled
        #
        # if not payment_type_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_PAYMENT_TYPE_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return payment_type_object

    def get(self, request, *args, **kwargs):
        payment_type = self.get_object()

        serializer = self.serializer_class(instance=payment_type,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=payment_type,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(PAYMENT_TYPE_DETAILS),
                              "data": serializer.data})

    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        payment_type = self.get_object()

        payment_type_id = self.kwargs.get("payment_type_id")
        serializer = self.serializer_class(
                            instance=payment_type,
                            data=request.data,
                            partial=True,
                            context={"payment_type_id": payment_type_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(PAYMENT_TYPE_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(PAYMENT_TYPE_NOT_UPDATED_MSG),
                              "data": serializer.errors})

    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        payment_type = self.get_object()

        payment_type_id = self.kwargs.get("payment_type_id")
        serializer = self.serializer_class(
                            instance=payment_type,
                            data=request.data,
                            partial=True,
                            context={"payment_type_id": payment_type_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(PAYMENT_TYPE_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(PAYMENT_TYPE_NOT_UPDATED_MSG),
                              "data": serializer.errors})

class PaymentTypeByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = PaymentTypeRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self):
        payment_type_id = self.kwargs.get("payment_type_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        payment_type_object = get_object_or_404(PaymentType,
                                                 id=payment_type_id)  # As one dictionary object, with exception

        # payment_type_object = PaymentType.objects.filter(id=payment_type_id).first()  # As one dictionary object, exception should be handled
        # payment_type_object = PaymentType.objects.filter(id=payment_type_id)  # As list with a dictionary element, exception should be handled
        #
        # if not payment_type_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_PAYMENT_TYPE_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return payment_type_object

    def get(self, request, *args, **kwargs):
        payment_type = self.get_object()

        serializer = self.serializer_class(instance=payment_type,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=payment_type,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(PAYMENT_TYPE_DETAILS),
                              "data": serializer.data})

    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)})

        payment_type = self.get_object()
        payment_type.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(PAYMENT_TYPE_DELETED_MSG),
                              "data": {}
                              })
