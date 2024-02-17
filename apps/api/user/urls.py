from django.urls import path
from apps.api.user.views import (ListAllUsersGenericList,
                                 RegisterNewUserGenericCreate,
                                 RegisterNewSuperUserGenericCreate,
                                 RegisterNewStaffUserGenericCreate,
                                 RegisterNewTrainerUserGenericCreate,
                                 _Test_RegisterNewUserGenericCreate,
                                 _Test_RegisterNewSuperUserGenericCreate,
                                 _Test_RegisterNewStaffUserGenericCreate,
                                 _Test_RegisterNewTrainerUserGenericCreate,
                                 )

app_name = "user"

urlpatterns = [
    # superuser
    path("list_all_users/", ListAllUsersGenericList.as_view(), name="list-all-users"),
    path("register_new_superuser/", RegisterNewSuperUserGenericCreate.as_view(), name="register-new-superuser"),

    # staff, superuser
    path("register_new_user/", RegisterNewUserGenericCreate.as_view(), name="register-new-user"),
    path("register_new_staff_user/", RegisterNewStaffUserGenericCreate.as_view(), name="register-new-staff-user"),
    path("register_new_staff_user/", RegisterNewStaffUserGenericCreate.as_view(), name="register-new-staff-user"),
    path("register_new_trainer_user/", RegisterNewTrainerUserGenericCreate.as_view(), name="register-new-trainer-user"),

    # ################### MY TRIAL CODE ################################
    path("_test_register_new_user_v2/", _Test_RegisterNewUserGenericCreate.as_view(), name="test-register-new-user-v2"),
    path("_test_register_new_staff_user_v2/", _Test_RegisterNewStaffUserGenericCreate.as_view(), name="test-register-new-staff-user-2"),
    path("_test_register_new_trainer_user_v2/", _Test_RegisterNewTrainerUserGenericCreate.as_view(), name="test-register-new-trainer-user-v2"),
    path("_test_register_new_superuser_v2/", _Test_RegisterNewSuperUserGenericCreate.as_view(), name="test-register-new-superuser-v2"),
    # ##################################################################

]
