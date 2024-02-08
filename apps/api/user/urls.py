from django.urls import path
from apps.api.user.views import ListAllUsersGenericList

app_name = "user"

urlpatterns = [
    path("list_all_users/", ListAllUsersGenericList.as_view(), name="list-all-users")
]
