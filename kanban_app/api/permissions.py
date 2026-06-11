from rest_framework.permissions import BasePermission

class IsOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return obj.owner == request.user
        return obj.owner == request.user or request.user in obj.members.all()