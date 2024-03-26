from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_actions import (NO_PAYMENT_DOCUMENTS_MSG,
                                                    ALL_PAYMENT_DOCUMENTS_MSG,
                                                    PAYMENT_DOCUMENT_CREATED_MSG,
                                                    PAYMENT_DOCUMENT_NOT_CREATED_MSG,
                                                    NO_PAYMENT_DOCUMENT_WITH_ID_MSG,
                                                    PAYMENT_DOCUMENT_DETAILS,
                                                    PAYMENT_DOCUMENT_UPDATED_MSG,
                                                    PAYMENT_DOCUMENT_NOT_UPDATED_MSG,
                                                    PAYMENT_DOCUMENT_DELETED_MSG
                                                    )

from apps.api.messages_api.messages_errors import (
                                    NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)

from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveDestroyAPIView,
                                     )

from apps.api.payment_document.serializers import (
                        PaymentDocumentAllFieldsModelSerializer,
                        PaymentDocumentCreateModelSerializer,
                        PaymentDocumentRetrieveUpdateDeleteModelSerializer)

from apps.api.payment_document.models import PaymentDocument

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from apps.api.authentication.permissions_custom import (IsSuperuser,
                                                        IsAdministrator,
                                                        IsCoach,
                                                        IsClient,
                                                        IsActive,
                                                        IsVerified)


class AllPaymentDocumentsGenericList(ListAPIView):
    serializer_class = PaymentDocumentAllFieldsModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_queryset(self):
        companies = PaymentDocument.objects.filter()
        return companies

    def get(self, request: Request, *args, **kwargs):
        companies = self.get_queryset()

        if not companies:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={"message": gettext_lazy(NO_PAYMENT_DOCUMENTS_MSG),
                                  "data": []}
                            )

        serializer = self.serializer_class(instance=companies,
                                           many=True)  # IMPORTANT: DON'T FORGET many=True
        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(ALL_PAYMENT_DOCUMENTS_MSG),
                              "data": serializer.data}
                        )



class CreateNewPaymentDocumentGenericCreate(CreateAPIView):
    serializer_class = PaymentDocumentCreateModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": self.request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(PAYMENT_DOCUMENT_CREATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(PAYMENT_DOCUMENT_NOT_CREATED_MSG),
                              "data": serializer.errors})



class PaymentDocumentByIdGenericRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = PaymentDocumentRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self, *args, **kwargs):
        payment_document_id = self.kwargs.get("payment_document_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        payment_document_object = get_object_or_404(PaymentDocument,
                                                 id=payment_document_id)  # As one dictionary object, with exception

        # payment_document_object = PaymentDocument.objects.filter(id=payment_document_id).first()  # As one dictionary object, exception should be handled
        # payment_document_object = PaymentDocument.objects.filter(id=payment_document_id)  # As list with a dictionary element, exception should be handled
        #
        # if not payment_document_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_PAYMENT_DOCUMENT_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return payment_document_object

    def get(self, request, *args, **kwargs):
        payment_document = self.get_object()

        serializer = self.serializer_class(instance=payment_document,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=payment_document,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(PAYMENT_DOCUMENT_DETAILS),
                              "data": serializer.data})

    def patch(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        payment_document = self.get_object()

        payment_document_id = self.kwargs.get("payment_document_id")
        serializer = self.serializer_class(
                            instance=payment_document,
                            data=request.data,
                            partial=True,
                            context={"payment_document_id": payment_document_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(PAYMENT_DOCUMENT_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(PAYMENT_DOCUMENT_NOT_UPDATED_MSG),
                              "data": serializer.errors})

    def put(self, request, *args, **kwargs):  # IMPORTANT: Only if PATCH, entered values stay after validation
        payment_document = self.get_object()

        payment_document_id = self.kwargs.get("payment_document_id")
        serializer = self.serializer_class(
                            instance=payment_document,
                            data=request.data,
                            partial=True,
                            context={"payment_document_id": payment_document_id,
                                     # Additionally transferred for serializer validation
                                     "request": self.request,
                                     }
                            )

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK,
                            data={"message": gettext_lazy(PAYMENT_DOCUMENT_UPDATED_MSG),
                                  "data": serializer.data})

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": gettext_lazy(PAYMENT_DOCUMENT_NOT_UPDATED_MSG),
                              "data": serializer.errors})

class PaymentDocumentByIdGenericRetrieveDestroy(RetrieveDestroyAPIView):
    serializer_class = PaymentDocumentRetrieveUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated, IsActive,
                          IsSuperuser | IsAdministrator | IsCoach]

    def get_object(self):
        payment_document_id = self.kwargs.get("payment_document_id")  # Training_group id from the request additional parameter
        # user_id = self.request.user.id  # Current user id from the request body

        payment_document_object = get_object_or_404(PaymentDocument,
                                                 id=payment_document_id)  # As one dictionary object, with exception

        # payment_document_object = PaymentDocument.objects.filter(id=payment_document_id).first()  # As one dictionary object, exception should be handled
        # payment_document_object = PaymentDocument.objects.filter(id=payment_document_id)  # As list with a dictionary element, exception should be handled
        #
        # if not payment_document_object:
        #     return Response(status=status.HTTP_404_NOT_FOUND,
        #                     data={"message": gettext_lazy(NO_PAYMENT_DOCUMENT_WITH_ID_MSG),
        #                           "data": {}
        #                           })

        return payment_document_object

    def get(self, request, *args, **kwargs):
        payment_document = self.get_object()

        serializer = self.serializer_class(instance=payment_document,  # If one dictionary object, got with get_or_404()
                                           context={"request": self.request})
        # serializer=self.serializer_class(instance=payment_document,
        #                                  many=True,
        #                                  context={"request":self.request})  # If list with one dictionary element, got with filter()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(PAYMENT_DOCUMENT_DETAILS),
                              "data": serializer.data})

    def delete(self, request, *args, **kwargs):
        user_is_superuser = request.user.is_superuser
        if not user_is_superuser:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": gettext_lazy(NOT_SUPERUSER_HARD_DELETE_FORBIDDEN)})

        payment_document = self.get_object()
        payment_document.delete()

        return Response(status=status.HTTP_200_OK,
                        data={"message": gettext_lazy(PAYMENT_DOCUMENT_DELETED_MSG),
                              "data": {}
                              })
