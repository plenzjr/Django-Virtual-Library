from django.urls import path
from .apis.views import RegisterView, ActiveUsersView, AllUsersView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('users/all/', AllUsersView.as_view(), name='all-users'),
    path('users/active/', ActiveUsersView.as_view(), name='active-users'),
]
