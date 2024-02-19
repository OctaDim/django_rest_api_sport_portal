from django.urls import path
from apps.api.user.views import (AllUsersGenericListForStaff,
                                 AllUsersGenericListForSuperuser,
                                 RegisterNewUserGenericCreate,
                                 RegisterNewSuperUserGenericCreate,
                                 RegisterNewStaffUserGenericCreate,
                                 RegisterNewTrainerUserGenericCreate,
                                 UserInfoByIdGenericRetrieveUpdDestroy,
                                 UserInfoByIdGenericRetrieveUpdate,
                                 _Test_RegisterNewUserGenericCreate,
                                 _Test_RegisterNewSuperUserGenericCreate,
                                 _Test_RegisterNewStaffUserGenericCreate,
                                 _Test_RegisterNewTrainerUserGenericCreate,
                                 )

app_name = "user"

urlpatterns = [
    # superuser
    path("register_new_superuser/", RegisterNewSuperUserGenericCreate.as_view(), name="register-new-superuser"),
    path("list_all_users_all_fields/", AllUsersGenericListForSuperuser.as_view(), name="list-all-users-all-fields"),
    path("user_info_by_id_hard_del/<int:user_id>/", UserInfoByIdGenericRetrieveUpdDestroy.as_view(), name="user-info-by-id-hard-del"),

    # staff, superuser
    path("register_new_user/", RegisterNewUserGenericCreate.as_view(), name="register-new-user"),
    path("register_new_staff_user/", RegisterNewStaffUserGenericCreate.as_view(), name="register-new-staff-user"),
    path("register_new_trainer_user/", RegisterNewTrainerUserGenericCreate.as_view(), name="register-new-trainer-user"),
    path("list_all_users_limit_fields/", AllUsersGenericListForStaff.as_view(), name="list-all-users-limit-fields"),
    path("user_info_by_id_soft_del/<int:user_id>/", UserInfoByIdGenericRetrieveUpdate.as_view(), name="user-info-by-id-soft-del"),

    # ################### MY TRIAL CODE ################################
    path("_test_register_new_user_v2/", _Test_RegisterNewUserGenericCreate.as_view(), name="test-register-new-user-v2"),
    path("_test_register_new_staff_user_v2/", _Test_RegisterNewStaffUserGenericCreate.as_view(), name="test-register-new-staff-user-2"),
    path("_test_register_new_trainer_user_v2/", _Test_RegisterNewTrainerUserGenericCreate.as_view(), name="test-register-new-trainer-user-v2"),
    path("_test_register_new_superuser_v2/", _Test_RegisterNewSuperUserGenericCreate.as_view(), name="test-register-new-superuser-v2"),
    # ##################################################################

]
