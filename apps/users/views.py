from django.shortcuts import render
from django.middleware.csrf import get_token
from django.contrib.auth import login, logout
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, UserMeSerializer

# Create your views here.

class CsrfView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # This sets/returns a CSRF token and also ensures csrftoken cookie is set
        token = get_token(request)
        return Response({"csrfToken": token}, status=status.HTTP_200_OK)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)  
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        login(request, user)
        return Response({"detail": "Login successful."}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserMeSerializer(request.user).data, status=status.HTTP_200_OK)