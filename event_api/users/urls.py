from django.urls import path
from .views import SignUpView, LoginView, LogoutView, MeView, UpdateUserView

urlpatterns = [
    path("auth/signup_user", SignUpView.as_view()),
    path("auth/login", LoginView.as_view()),
    path("auth/logout", LogoutView.as_view()),
    path("users/me", MeView.as_view()),
    path("users/<uuid:id>", UpdateUserView.as_view(), name="update-user"),
]
