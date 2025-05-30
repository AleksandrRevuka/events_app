from django.db import models

from users.models import User
from events.models import Event

class EventRegistration(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="registrations"
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="registrations"
    )

    def __str__(self):
        return f"{self.user.email} registered for {self.event.title}"
