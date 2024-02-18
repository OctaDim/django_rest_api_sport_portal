from django.urls import path
from apps.api.user.views import (ListAllUsersGenericList,
                                 RegisterNewUserGenericCreate,
                                 RegisterNewSuperUserGenericCreate,
                                 RegisterNewStaffUserGenericCreate,
                                 RegisterNewTrainerUserGenericCreate,
                                 UserInfoByIdGenericRetrieveUpdDestroy,
                                 _Test_RegisterNewUserGenericCreate,
                                 _Test_RegisterNewSuperUserGenericCreate,
                                 _Test_RegisterNewStaffUserGenericCreate,
                                 _Test_RegisterNewTrainerUserGenericCreate,
                                 )

app_name = "user"

urlpatterns = [
    # superuser
    path("register_new_superuser/", RegisterNewSuperUserGenericCreate.as_view(), name="register-new-superuser"),
    path("user_info_by_id_hard/<int:user_id>/", UserInfoByIdGenericRetrieveUpdDestroy.as_view(), name="get-user-info-by-id-hard"),

    # staff, superuser
    path("register_new_user/", RegisterNewUserGenericCreate.as_view(), name="register-new-user"),
    path("register_new_staff_user/", RegisterNewStaffUserGenericCreate.as_view(), name="register-new-staff-user"),
    path("register_new_trainer_user/", RegisterNewTrainerUserGenericCreate.as_view(), name="register-new-trainer-user"),
    path("list_all_users/", ListAllUsersGenericList.as_view(), name="list-all-users"),

    # ################### MY TRIAL CODE ################################
    path("_test_register_new_user_v2/", _Test_RegisterNewUserGenericCreate.as_view(), name="test-register-new-user-v2"),
    path("_test_register_new_staff_user_v2/", _Test_RegisterNewStaffUserGenericCreate.as_view(), name="test-register-new-staff-user-2"),
    path("_test_register_new_trainer_user_v2/", _Test_RegisterNewTrainerUserGenericCreate.as_view(), name="test-register-new-trainer-user-v2"),
    path("_test_register_new_superuser_v2/", _Test_RegisterNewSuperUserGenericCreate.as_view(), name="test-register-new-superuser-v2"),
    # ##################################################################

]
