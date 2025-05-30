from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "event_date",
            "location",
            "organizer",
            "author",
        ]
        read_only_fields = ["id", "author"]


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "event_date",
            "location",
            "organizer",
        ]


class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "event_date",
            "location",
            "organizer",
        ]
