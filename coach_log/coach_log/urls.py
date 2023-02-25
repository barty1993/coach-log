"""coach_log URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import RegisterView, GetAuthUserAPIView, UpdateUserAPIView, CustomTokenObtainPairView
from gum.views import ListGumAPIView, CreateUpdateGumAPIView, AddKindOfSportAPIView, ListGumForAuthUserAPIView, \
    InviteCoachAPIView, DetailGumAPIView
from log.views import CreateUpdateAthleteAPIView, GroupAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    # accounts
    path('api/registration/', RegisterView.as_view(), name="registration"),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/user/', GetAuthUserAPIView.as_view(), name='get auth user'),
    path('api/user/update/<int:pk>/', UpdateUserAPIView.as_view(), name='update user'),

    path('api/gum/', ListGumAPIView.as_view(), name='get all gums'),
    path('api/gum/<int:pk>/', DetailGumAPIView.as_view(), name='get detail gum'),
    path('api/gum/auth/', ListGumForAuthUserAPIView.as_view(), name='get all gum for auth user'),
    path('api/gum/create/', CreateUpdateGumAPIView.as_view(), name='create gum'),
    path('api/gum/update/<int:pk>/', CreateUpdateGumAPIView.as_view(), name='update gum'),
    path('api/gum/add/kindofsport/<int:pk>/', AddKindOfSportAPIView.as_view(), name='add kind of sport'),
    path('api/gum/invite/coach/', InviteCoachAPIView.as_view(), name='invite coach in gum'),
    path('api/gum/invite/coach/<int:pk>/', InviteCoachAPIView.as_view(), name='update or delete invites'),

    path('api/athlete/', CreateUpdateAthleteAPIView.as_view(), name='create Athlete'),
    path('api/athlete/<int:pk>/', CreateUpdateAthleteAPIView.as_view(), name='update Athlete'),
    path('api/group/', GroupAPIView.as_view(), name='create, update, delete Group'),
    path('api/group/<int:pk>/', GroupAPIView.as_view()),
]
