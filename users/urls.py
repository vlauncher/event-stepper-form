from django.urls import path
from .views import (
    LoginView,
    RegisterView,
    HomePageView,
    LogoutView,
    VerifyEmailView,
    ChangePasswordView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "verify-email/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify_email"
    ),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]
