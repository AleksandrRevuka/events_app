from django.urls import path
from .views import SignUpView, LoginView, LogoutView, MeView, UpdateUserView

urlpatterns = [
    path("signup_user", SignUpView.as_view()),
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),
    path("me", MeView.as_view()),
    path("<uuid:id>", UpdateUserView.as_view(), name='update-user')
]
