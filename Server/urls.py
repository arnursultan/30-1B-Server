from django.urls import path
from .views import (
    LoginView,
    CustomTokenRefreshView,
    LogoutView,
    MeView,
    AdultOnlySecretView,
    UniversalSocialJWTLogin
)

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="auth_login"),
    path("auth/refresh/", CustomTokenRefreshView.as_view(), name="auth_refresh"),
    path("auth/logout/", LogoutView.as_view(), name="auth_logout"),
    path("me/", MeView.as_view(), name="me"),
    path("secrets/adults-only/", AdultOnlySecretView.as_view(), name="adults_only"),
    path("social/<str:provider>/", UniversalSocialJWTLogin.as_view(), name="social_login"),
]