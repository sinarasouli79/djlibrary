from rest_framework.permissions import BasePermission

from library.models import Librarian


class IsLibrarian(BasePermission):

    def has_permission(self, request, view):
        user_id = request.user.id
        return Librarian.objects.filter(user_id=user_id).exists()
