from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import (
    UserCreateSerializer,
    UserResponseSerializer,
    UserUpdateSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    inline_serializer,
)



class SignUpView(APIView):
    @extend_schema(
        request=UserCreateSerializer,
        responses=UserResponseSerializer,
        tags=["Users: Authentication"],
        operation_id="user_sign_up",
        summary="User sign up",
    )
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserResponseSerializer(user).data, status=status.HTTP_201_CREATED
        )


class TokenResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


@extend_schema(
    request=inline_serializer(
        name="LoginRequest",
        fields={
            "username": serializers.EmailField(),
            "password": serializers.CharField(),
        },
    ),
    responses={
        200: OpenApiResponse(
            response=TokenResponseSerializer,
            description="Returns JWT access and refresh tokens.",
        ),
        401: OpenApiResponse(description="Invalid credentials."),
    },
    tags=["Users: Authentication"],
    operation_id="user_login",
    summary="User login to get JWT tokens",
)
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if not user:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {"access_token": str(refresh.access_token)}, status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    @extend_schema(
        responses={
            200: OpenApiResponse(description="Successfully logged out."),
        },
        tags=["Users: Authentication"],
        operation_id="user_logout",
        summary="User logout",
    )
    def get(self, request):
        response = Response(
            {"detail": "Successfully logged out"}, status=status.HTTP_200_OK
        )
        response.delete_cookie("access_token")
        return response


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses=UserResponseSerializer,
        tags=["Users: Profile"],
        operation_id="user_me",
        summary="User information",
    )
    def get(self, request):
        serializer = UserResponseSerializer(request.user)
        return Response(serializer.data)


class UpdateUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        return get_object_or_404(User, id=id)

    @extend_schema(
        responses=UserResponseSerializer,
        tags=["Users: Profile"],
        operation_id="user_update",
        summary="Update user information",
    )
    def put(self, request, id):
        user = self.get_object(id)
        if request.user != user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UserUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        responses=UserResponseSerializer,
        tags=["Users: Profile"],
        operation_id="user_delete",
        summary="Delete user",
    )
    def delete(self, request, id):
        user = self.get_object(id)
        if request.user != user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
