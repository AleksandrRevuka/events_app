from rest_framework.permissions import BasePermission
from users.models import Role


class IsOrganizer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.ORGANIZER
