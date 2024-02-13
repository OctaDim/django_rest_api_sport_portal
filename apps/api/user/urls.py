from django.urls import path
from apps.api.user.views import (ListAllUsersGenericList,
                                 RegisterNewUserGenericCreate,
                                 RegisterNewSuperUserGenericCreate,
                                 RegisterNewStaffUserGenericCreate,
                                 __TEST_RegisterNewUserGenericCreate,
                                 __TEST_RegisterNewSuperUserGenericCreate,
                                 __TEST_RegisterNewStaffUserGenericCreate,
                                 )

app_name = "user"

urlpatterns = [
    path("list_all_users/", ListAllUsersGenericList.as_view(), name="list-all-users"),
    path("register_new_user/", RegisterNewUserGenericCreate.as_view(), name="register-new-user"),
    path("register_new_superuser/", RegisterNewSuperUserGenericCreate.as_view(), name="register-new-superuser"),
    path("register_new_staff_user/", RegisterNewStaffUserGenericCreate.as_view(), name="register-new-staff-user"),

    # ################### TRIAL CODE ###################################
    path("__TEST_register_new_user_v2/", __TEST_RegisterNewUserGenericCreate.as_view(), name="TEST-register-new-user-v2"),
    path("__TEST_register_new_superuser_v2/", __TEST_RegisterNewSuperUserGenericCreate.as_view(), name="TEST-register-new-superuser-v2"),
    path("__TEST_register_new_staff_user_v2/", __TEST_RegisterNewStaffUserGenericCreate.as_view(), name="TEST-register-new-staff-user-2"),
    # ##################################################################

    # path("", as_view(), name=""),
    # path("", as_view(), name=""),
    # path("", as_view(), name=""),
    # path("", as_view(), name=""),

]
