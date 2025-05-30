from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .permissions import IsOrganizer
from .serializers import EventCreateSerializer, EventSerializer, EventUpdateSerializer
from .models import Event


class EventListView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=EventSerializer(many=True), description="List of all events."
            )
        },
        tags=["Events"],
        operation_id="list_events",
        summary="Get list of events",
        description="Returns a list of all available events. Publicly accessible.",
    )
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=EventSerializer, description="Event details."
            ),
            404: OpenApiResponse(description="Event not found."),
        },
        tags=["Events"],
        operation_id="get_event_detail",
        summary="Get single event",
        description="Returns detailed information about a specific event by ID.",
    )
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @extend_schema(
        request=EventCreateSerializer,
        responses={
            201: OpenApiResponse(
                response=EventSerializer, description="Event created successfully."
            ),
            400: OpenApiResponse(description="Invalid input data."),
            403: OpenApiResponse(description="User is not an organizer."),
        },
        tags=["Events"],
        operation_id="create_event",
        summary="Create new event",
        description="Allows authenticated users with organizer permissions to create a new event.",
    )
    def post(self, request):
        serializer = EventCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @extend_schema(
        request=EventUpdateSerializer,
        responses={
            200: OpenApiResponse(
                response=EventSerializer, description="Event updated successfully."
            ),
            400: OpenApiResponse(description="Invalid input data."),
            403: OpenApiResponse(description="Permission denied."),
            404: OpenApiResponse(description="Event not found."),
        },
        tags=["Events"],
        operation_id="update_event",
        summary="Update event",
        description="Allows event authors to update their events. Organizer permission required.",
    )
    def put(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if event.author != request.user:
            return Response(
                {"detail": "You do not have permission to update this event."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = EventUpdateSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @extend_schema(
        responses={
            204: OpenApiResponse(description="Event deleted successfully."),
            403: OpenApiResponse(description="Permission denied."),
            404: OpenApiResponse(description="Event not found."),
        },
        tags=["Events"],
        operation_id="delete_event",
        summary="Delete event",
        description="Allows event authors to delete their events. Organizer permission required.",
    )
    def delete(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if event.author != request.user:
            return Response(
                {"detail": "You do not have permission to delete this event."},
                status=status.HTTP_403_FORBIDDEN,
            )
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
