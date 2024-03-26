from django.urls import path

from apps.api.payment_type.views import (
                            AllPaymentTypesGenericList,
                            CreateNewPaymentTypeGenericCreate,
                            PaymentTypeByIdGenericRetrieveUpdate,
                            PaymentTypeByIdGenericRetrieveDestroy,
                            )

app_name = "payment_types"

urlpatterns = [
   path("all_payment_types/",
         AllPaymentTypesGenericList.as_view(),
         name="list-all-payment-types"),

    path("create_new_payment_type/",
         CreateNewPaymentTypeGenericCreate.as_view(),
         name="create-new-payment_type"),

    path("payment_type_by_id_soft/<int:payment_type_id>/",
         PaymentTypeByIdGenericRetrieveUpdate.as_view(),
         name="payment_type-by-id-soft"),

    path("payment_type_by_id_hard/<int:payment_type_id>/",
         PaymentTypeByIdGenericRetrieveDestroy.as_view(),
         name="payment_type-by-id-hard"),

]
