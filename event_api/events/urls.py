from django.urls import path
from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
)

urlpatterns = [
    path("events/", EventListView.as_view(), name="event-list"),
    path("events/<int:event_id>/", EventDetailView.as_view(), name="event-detail"),
    path("events/create/", EventCreateView.as_view(), name="event-create"),
    path(
        "events/<int:event_id>/update/", EventUpdateView.as_view(), name="event-update"
    ),
    path(
        "events/<int:event_id>/delete/", EventDeleteView.as_view(), name="event-delete"
    ),
]
