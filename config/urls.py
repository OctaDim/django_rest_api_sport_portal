"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.conf.urls.static import static  # Added
from django.conf import settings  # Added

from django.urls import path, include, re_path  # Added include

# ######################### FOR SWAGGER #######################################
from drf_yasg import openapi  # Added
from drf_yasg.views import get_schema_view  # Added
from rest_framework.permissions import (IsAdminUser,  # API can read/write only admin
                                        IsAuthenticatedOrReadOnly,  # API can read/write authorised, else readonly
                                        AllowAny,  # API can read/write any users (allowed to all)
                                        # BasePermission,  # API can read/write only (custom settings)
                                        IsAuthenticated,  # API can read/write only authorised users
                                        )

# ######################### FOR SWAGGER #######################################
schema_view = get_schema_view(
    info=openapi.Info(title="SPORT PORTAL API Documentation",
                      default_version="v1.0",
                      description="SPORT PORTAL APPLICATION API DOCUMENTATION",
                      terms_of_service="#",  # for example, https://www.domain.com/api/terms
                      contact=openapi.Contact(email="octadim@gmail.com"),
                      license=openapi.License(name="LICENSE")
                      ),

    public=True,  # API settings (public or not)
    # permission_classes=([IsAuthenticated, IsAdminUser, ])  # Can be added several permissions
    permission_classes = ([AllowAny])  # Can be added several permissions  # Other options bellow
    # permission_classes = ([IsAdminUser])  # Can be added several permissions
    # permission_classes = ([IsAuthenticated])  # Can be added several permissions
    # permission_classes = ([IsAuthenticatedOrReadOnly])  # Can be added several permissions
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include("apps.api.router")),  # IMPORTANT: DON'T FORGET TO ADD .router to the end

    # ######### SWAGGER URLS #################
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="swagger-json"),
    re_path(r"^swagger/$", schema_view.with_ui('swagger', cache_timeout=0), name="swagger-ui"),
    re_path(r"^redoc/$", schema_view.with_ui('redoc', cache_timeout=0), name="redoc-ui"),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Added
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Added

if not settings.DEBUG:  # Plug template, if url was not found, also define in settings MIDDLEWARE and INSTALLED_APPS
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
