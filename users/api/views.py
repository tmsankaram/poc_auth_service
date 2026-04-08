from typing import Any

from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from models import CustomUser
from serializers import UserModelSerializer


class UserProfileListCreateView(ListCreateAPIView):
    """Generic View for listing and creating user profiles"""

    queryset = CustomUser.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [AllowAny]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        credentials = {"email": attrs.get("email"), "password": attrs.get("password")}

        user = authenticate(**credentials)

        if user:
            if not user.is_active:
                raise exceptions.AuthenticationFailed("Account is deactivated")

            data = {}
            refresh = self.get_token(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            return data
        else:
            raise exceptions.AuthenticationFailed("Invalid Credentials")


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
