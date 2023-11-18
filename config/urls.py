"""
URL configuration for virtual_library project.

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
from django.contrib.auth import views
from django.contrib.auth.decorators import permission_required
from django.urls import path, re_path, include
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Django Virtual Library API",
        default_version='v1',
        description="Simple API for a virtual library",
        contact=openapi.Contact(email="contact@myapp.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # path('', views.index, name='index'),
    # Auth
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # Admin
    path('admin/', admin.site.urls),
    # Acount
    path('account/', include('app_account.urls')),
    # Library
    path('library/', include('app_library.urls')),
    # Swagger Docs
    path(
        'swagger/',
        permission_required(
            'permissions.IsAdminUser',
            login_url="../login"
        )
        (
            schema_view.with_ui(
                'swagger',
                cache_timeout=0
            )
        ),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        permission_required(
            'permissions.IsAdminUser',
            login_url="../login"
        )
        (
            schema_view.with_ui(
                'redoc',
                cache_timeout=0
            )
        ),
        name='schema-redoc'
    ),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        permission_required(
            'permissions.IsAdminUser',
            login_url="../login"
        )
        (
            schema_view.without_ui(cache_timeout=0)
        ),
        name='schema-json'
    ),
]
