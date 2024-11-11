from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetConfirmView
from django.urls import path, reverse_lazy

from .forms import (
    LoginForm,
    # NewPasswordForm
)
from .views import (
    RegisterView,
    ProfileView, ProfileUpdateView, ProfileDetailView, ProfileListView
)

app_name = "account"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            authentication_form=LoginForm,
            template_name="account/login.html",
            redirect_authenticated_user=True,

        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(
            template_name="index.html",
            next_page=reverse_lazy("account:login"),
        ),
        name="logout",
    ),
    path("register/", RegisterView.as_view(), name="register"),

    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/<uuid:pk>/", ProfileDetailView.as_view(), name="profile_details"),
    path("profile/<uuid:pk>/update/", ProfileUpdateView.as_view(), name="profile_update"),
    path("profile/profile_list", ProfileListView.as_view(), name="profile_list"),

    # path(
    #     "restore_account/email/",
    #     UserForgotPasswordView.as_view(),
    #     name="password_reset",
    # ),
    #     path(
    #         "restore_account/new-password/<uidb64>/<token>/",
    #         PasswordResetConfirmView.as_view(
    #             template_name="password.html",
    #             form_class=NewPasswordForm,
    #             success_url=reverse_lazy("account:login"),
    #         ),
    #         name="password_reset_confirm",
    #     ),

]
