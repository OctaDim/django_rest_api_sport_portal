from django.urls import path

from apps.api.payment_document.views import (
                            AllPaymentDocumentsGenericList,
                            CreateNewPaymentDocumentGenericCreate,
                            PaymentDocumentByIdGenericRetrieveUpdate,
                            PaymentDocumentByIdGenericRetrieveDestroy,
                            )

app_name = "payment_documents"

urlpatterns = [
   path("all_payment_documents/",
         AllPaymentDocumentsGenericList.as_view(),
         name="list-all-payment-documents"),

    path("create_new_payment_document/",
         CreateNewPaymentDocumentGenericCreate.as_view(),
         name="create-new-payment_document"),

    path("payment_document_by_id_soft/<int:payment_document_id>/",
         PaymentDocumentByIdGenericRetrieveUpdate.as_view(),
         name="payment_document-by-id-soft"),

    path("payment_document_by_id_hard/<int:payment_document_id>/",
         PaymentDocumentByIdGenericRetrieveDestroy.as_view(),
         name="payment_document-by-id-hard"),

]
