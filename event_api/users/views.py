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
        responses={
            201: UserResponseSerializer,
            400: OpenApiResponse(description="Validation error."),
        },
        tags=["Users: Authentication"],
        operation_id="user_sign_up",
        summary="User sign up",
        description="Creates a new user and returns user data.",
    )
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserResponseSerializer(user).data, status=status.HTTP_201_CREATED
        )


class TokenResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


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
            response=inline_serializer(
                name="LoginResponse",
                fields={
                    "access_token": serializers.CharField(),
                },
            ),
            description="Returns JWT access token.",
        ),
        401: OpenApiResponse(description="Invalid credentials."),
    },
    tags=["Users: Authentication"],
    operation_id="user_login",
    summary="User login to get JWT tokens",
    description="Logs in a user using email and password. Returns a JWT access token.",
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
        description="Clears the JWT cookie (if any) and logs out the user.",
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
        responses={
            200: UserResponseSerializer,
            401: OpenApiResponse(description="Authentication required."),
        },
        tags=["Users: Profile"],
        operation_id="user_me",
        summary="User information",
        description="Returns the profile information of the currently authenticated user.",
    )
    def get(self, request):
        serializer = UserResponseSerializer(request.user)
        return Response(serializer.data)


class UpdateUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        return get_object_or_404(User, id=id)

    @extend_schema(
        request=UserUpdateSerializer,
        responses={
            200: UserResponseSerializer,
            400: OpenApiResponse(description="Validation error."),
            403: OpenApiResponse(description="Not allowed to update another user."),
            404: OpenApiResponse(description="User not found."),
        },
        tags=["Users: Profile"],
        operation_id="user_update",
        summary="Update user information",
        description="Allows the authenticated user to update their own profile.",
    )
    def put(self, request, id):
        user = self.get_object(id)
        if request.user != user:
            return Response(
                {"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = UserUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        responses={
            204: OpenApiResponse(description="User deleted successfully."),
            403: OpenApiResponse(description="Not allowed to delete another user."),
            404: OpenApiResponse(description="User not found."),
        },
        tags=["Users: Profile"],
        operation_id="user_delete",
        summary="Delete user",
        description="Allows the authenticated user to delete their own account.",
    )
    def delete(self, request, id):
        user = self.get_object(id)
        if request.user != user:
            return Response(
                {"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN
            )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
