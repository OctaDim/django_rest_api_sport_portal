from django.urls import path, include

app_name = "router"

urlpatterns = [
    path('users/', include("apps.api.user")),

]
