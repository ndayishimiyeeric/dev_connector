from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from djoser.social.views import ProviderAuthView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access = response.data.get('access')
            refresh = response.data.get('refresh')

            response.set_cookie(
                'access',
                access,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

            response.set_cookie(
                'refresh',
                refresh,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            request.data["refresh"] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access = response.data.get("access")

            response.set_cookie(
                'access',
                access,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs) -> Response:
        access = request.COOKIES.get("access")

        if access:
            request.data["token"] = access

        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs) -> Response:
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


@api_view(['GET'])
def get_routes(request):
    routes = [
        {'GET': '/api/products'},
    ]
    return Response(routes)