"""Custom permission classes for board, task and comment access."""

from rest_framework.permissions import BasePermission
from kanban_app.models import Board, Task


class IsOwnerOrMember(BasePermission):
    """Allow the board owner or its members; only the owner may delete."""

    def has_object_permission(self, request, view, obj):
        """Owner may always act; members for every non-delete method."""
        if request.method == "DELETE":
            return obj.owner == request.user
        return obj.owner == request.user or request.user in obj.members.all()


class IsBoardMember(BasePermission):
    """Allow only the owner/members of the board named in the request body."""

    def has_permission(self, request, view):
        """Check membership against the board id sent in the request data."""
        board_id = request.data.get('board')
        board = Board.objects.filter(id=board_id).first()
        if not board:
            return False
        return (board.owner == request.user or
                request.user in board.members.all())


class IsCreatorOrOwner(BasePermission):
    """Board members may edit; only the creator or board owner may delete."""

    def has_object_permission(self, request, view, obj):
        """Delete: creator or board owner. Otherwise: any board member."""
        if request.method == "DELETE":
            return (obj.board.owner == request.user or
                    obj.creator == request.user)
        return (obj.board.owner == request.user or
                request.user in obj.board.members.all())


class IsTaskBoardMember(BasePermission):
    """Allow only the owner/members of the board owning the URL task."""

    def has_permission(self, request, view):
        """Resolve the task from the URL and check board membership."""
        task_id = view.kwargs.get('pk')
        task = Task.objects.filter(id=task_id).first()
        if not task:
            return False
        return (task.board.owner == request.user or
                request.user in task.board.members.all())


class IsAuthorOfComment(BasePermission):
    """Allow only the author of the comment."""

    def has_object_permission(self, request, view, obj):
        """Permit the action only for the comment's author."""
        return obj.author == request.user
