from rest_framework import permissions
from Application1.models import User

DO_NOT_HAVE_PERMISSION = "You do not have permission to do this action."

class IsEndUser(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            if User.objects.filter(id=request.user.id).exists():
                return True
        except Exception as e:
            return False        