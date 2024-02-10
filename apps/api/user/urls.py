from django.urls import path
from apps.api.user.views import (ListAllUsersGenericList,
                                 RegisterNewUserGenericCreate,
                                 )

app_name = "user"

urlpatterns = [
    path("list_all_users/", ListAllUsersGenericList.as_view(), name="list-all-users"),
    path("register_new_user", RegisterNewUserGenericCreate.as_view(), name="register-new-user"),
    # path("", as_view(), name=""),
    # path("", as_view(), name=""),
    # path("", as_view(), name=""),
    # path("", as_view(), name=""),
    # path("", as_view(), name=""),

]
