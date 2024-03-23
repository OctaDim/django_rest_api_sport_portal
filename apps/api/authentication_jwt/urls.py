from django.urls import path

from rest_framework_simplejwt.views import (TokenRefreshView,
                                            TokenVerifyView,
                                            TokenBlacklistView,
                                            TokenRefreshSlidingView,
                                            )

from apps.api.authentication_jwt.views import (CustomTokenObtainPairView,
                                               logout_function)


app_name = "authentication_jwt"

urlpatterns = [
    path("jwt_obtain_token/", CustomTokenObtainPairView.as_view(), name="jwt-obtain-token"),
    path("jwt_refresh_token/", TokenRefreshView.as_view(), name="jwt-refresh-token"),
    path("jwt_verify_token/", TokenVerifyView.as_view(), name="jwt-verify-token"),

    # COMMON LOGGING
    path("user_logout/", logout_function, name="user-logout"),

]
