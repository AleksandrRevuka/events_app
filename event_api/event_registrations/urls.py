from django.urls import path
from .views import (
    RegistrationListView,
    RegistrationCreateView,
    RegistrationDeleteView,
)

urlpatterns = [
    path("registrations/", RegistrationListView.as_view(), name="registration-list"),
    path(
        "registrations/create/",
        RegistrationCreateView.as_view(),
        name="registration-create",
    ),
    path(
        "registrations/<int:registration_id>/",
        RegistrationDeleteView.as_view(),
        name="registration-delete",
    ),
]
