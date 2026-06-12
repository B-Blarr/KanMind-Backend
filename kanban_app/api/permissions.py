from rest_framework.permissions import BasePermission
from kanban_app.models import Board, Task

class IsOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return obj.owner == request.user
        return obj.owner == request.user or request.user in obj.members.all()
    

class IsBoardMember(BasePermission):
    def has_permission(self, request, view):
        board_id = request.data.get('board')
        board = Board.objects.filter(id=board_id).first()
        if not board:
            return False
        return board.owner == request.user or request.user in board.members.all()
        
