from rest_framework.permissions import BasePermission

class IsOwnerForDelete(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return obj.owner == request.user
        return True