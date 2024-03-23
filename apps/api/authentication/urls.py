from django.urls import path

from apps.api.authentication_jwt.views import logout_function


app_name = "authentication"

urlpatterns = [
    path("user_logout/", logout_function, name="user-logout"),
]
