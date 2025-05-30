from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema

from .permissions import IsOrganizer
from .serializers import EventCreateSerializer, EventSerializer, EventUpdateSerializer
from .models import Event


class EventListView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={200: EventSerializer(many=True)},
        tags=["Events"],
        summary="Get list of events",
    )
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={200: EventSerializer},
        tags=["Events"],
        summary="Get single event",
    )
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @extend_schema(
        request=EventCreateSerializer,
        responses={201: EventSerializer},
        tags=["Events"],
        summary="Create new event",
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
        responses={200: EventSerializer},
        tags=["Events"],
        summary="Update event",
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
        responses={204: None}, tags=["Events"], summary="Delete event"
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
