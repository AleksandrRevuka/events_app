from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import EventRegistration
from .serializers import (
    EventRegistrationResponseSerializer,
    CreateEventRegistrationSerializer,
)
from events.models import Event
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema


class RegistrationListView(generics.ListAPIView):
    serializer_class = EventRegistrationResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EventRegistration.objects.filter(user=self.request.user)

    @extend_schema(
        tags=["Event Registrations"],
        summary="Get registrations",
        responses={200: EventRegistrationResponseSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RegistrationCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Event Registrations"],
        summary="Create new registration",
        request=CreateEventRegistrationSerializer,
        responses={201: EventRegistrationResponseSerializer},
    )
    def post(self, request):
        serializer = CreateEventRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = get_object_or_404(Event, id=serializer.validated_data["event"].id)

        if EventRegistration.objects.filter(user=request.user, event=event).exists():
            return Response(
                {"detail": "You are already registered for this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        registration = EventRegistration.objects.create(user=request.user, event=event)

        response_serializer = EventRegistrationResponseSerializer(registration)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class RegistrationDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={204: None},
        tags=["Event Registrations"],
        summary="Delete registration",
    )
    def delete(self, request, registration_id):
        registration = get_object_or_404(
            EventRegistration, id=registration_id
        )
        if registration.user != request.user:
            return Response(
                {"detail": "You do not have permission to delete this registration."},
                status=status.HTTP_403_FORBIDDEN,
            )
        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
