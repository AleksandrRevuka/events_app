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
from drf_spectacular.utils import extend_schema, OpenApiResponse


class RegistrationListView(generics.ListAPIView):
    serializer_class = EventRegistrationResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EventRegistration.objects.filter(user=self.request.user)

    @extend_schema(
        tags=["Event Registrations"],
        summary="Get registrations",
        description="Returns a list of event registrations associated with the authenticated user.",
        operation_id="list_event_registrations",
        responses={
            200: EventRegistrationResponseSerializer(many=True),
            401: OpenApiResponse(
                description="Authentication credentials were not provided or are invalid."
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RegistrationCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Event Registrations"],
        summary="Create new registration",
        description="Registers the authenticated user for a specific event. Prevents duplicate registrations.",
        operation_id="create_event_registration",
        request=CreateEventRegistrationSerializer,
        responses={
            201: EventRegistrationResponseSerializer,
            400: OpenApiResponse(
                description="User is already registered for this event or invalid data."
            ),
            401: OpenApiResponse(
                description="Authentication credentials were not provided or are invalid."
            ),
            404: OpenApiResponse(description="Event not found."),
        },
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
        tags=["Event Registrations"],
        summary="Delete registration",
        description="Deletes an existing event registration if it belongs to the authenticated user.",
        operation_id="delete_event_registration",
        responses={
            204: OpenApiResponse(description="Registration deleted successfully."),
            403: OpenApiResponse(
                description="Permission denied. You cannot delete someone else's registration."
            ),
            404: OpenApiResponse(description="Registration not found."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided or are invalid."
            ),
        },
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
