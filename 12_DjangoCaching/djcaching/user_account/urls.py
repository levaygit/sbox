from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    MyLogoutView,
    AboutMeView,
    RegisterView,
)


app_name = "user_account"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="user_account/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("about-me/<int:pk>/", AboutMeView.as_view(), name="about_me"),
    path("register/", RegisterView.as_view(), name="register"),
]
