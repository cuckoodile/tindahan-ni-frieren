"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from accounts.views import *

urlpatterns = [
    # Defaults
    path('admin/', admin.site.urls),
        # Token
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # User Endpoints
        # GET
    path('api/users/', UserListAPIView.as_view(), name='user_list_create'),
    path('api/users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user_retrieve_update_destroy'),
    path('api/profile/', OwnerListAPIView.as_view(), name='owner_profile'),
        # POST
    path('api/users/customer/', CustomerCreateAPIView.as_view(), name='customer_create'),
    path('api/users/staff/', StaffCreateAPIView.as_view(), name='staff_create'),
    path('api/users/admin/', AdminCreateAPIView.as_view(), name='admin_create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
