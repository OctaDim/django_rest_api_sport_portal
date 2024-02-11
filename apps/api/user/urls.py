from django.urls import path
from apps.api.user.views import (ListAllUsersGenericList,
                                 RegisterNewUserGenericCreate,
                                 RegisterNewSuperUserGenericCreate,
                                 RegisterNewStaffUserGenericCreate,
                                 )

app_name = "user"

urlpatterns = [
    path("list_all_users/", ListAllUsersGenericList.as_view(), name="list-all-users"),
    path("register_new_user/", RegisterNewUserGenericCreate.as_view(), name="register-new-user"),
    path("register_new_superuser/", RegisterNewSuperUserGenericCreate.as_view(), name="register-new-superuser"),
    path("register_new_staff_user/", RegisterNewStaffUserGenericCreate.as_view(), name="register-new-staff-user"),
    # path("", as_view(), name=""),
    # path("", as_view(), name=""),
    # path("", as_view(), name=""),
    # path("", as_view(), name=""),

]
