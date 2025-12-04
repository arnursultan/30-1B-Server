from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from .permissions import IsAdult

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter

from .social_serializers import CustomSocialLoginSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {"detail": "Поле 'refresh' обязательно"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"detail": "Невалидный или уже отозванный refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"detail": "Вы вышли из системы"}, status=status.HTTP_205_RESET_CONTENT)

class MeView(APIView):
    def get(self,request):
        user = request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

class AdultOnlySecretView(APIView):
    permission_classes = [IsAdult]

    def get(self, request):
        return Response(
            {
                "message": "Секретный ресурс только для совершеннолетних пользователей.",
                "user": UserSerializer(request.user).data,
            },
            status=status.HTTP_200_OK,
        )

PROVIDERS = {
    "google": GoogleOAuth2Adapter,
    "github": GitHubOAuth2Adapter,
}

class UniversalSocialJWTLogin(APIView):
    def post(self, request, provider):
        provider = provider.lower()

        if provider not in PROVIDERS:
            return Response(
                {"detail": f"Провайдер '{provider}' не поддерживается."},
                status=status.HTTP_400_BAD_REQUEST
            )

        adapter_class = PROVIDERS[provider]

        view = SocialLoginView.as_view(
            adapter_class=adapter_class,
            serializer_class=CustomSocialLoginSerializer
        )

        social_response = view(request._request)

        if social_response.status_code >= 400:
            return social_response

        user = social_response.context_data["user"]

        refresh = RefreshToken.for_user(user)

        data = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "provider": provider,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            },
        }

        return Response(data, status=200)