"""Views for the kanban API: boards, tasks and comments."""

from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from kanban_app.models import Board, Task, Comment
from .serializers import (
    BoardSerializer, BoardDetailReadSerializer, BoardDetailWriteSerializer,
    TaskSerializer, TaskDetailSerializer, CommentSerializer,
)
from .permissions import (
    IsOwnerOrMember, IsBoardMember, IsCreatorOrOwner,
    IsTaskBoardMember, IsAuthorOfComment,
)


class BoardView(generics.ListCreateAPIView):
    """List the boards the user owns or belongs to, and create new ones."""

    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def perform_create(self, serializer):
        """Set the creating user as the board owner."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Return boards where the user is owner or member (deduplicated)."""
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a single board (owner or member only)."""

    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrMember]

    def get_serializer_class(self):
        """Use the write serializer for PUT/PATCH, the read one otherwise."""
        if self.request.method in ('PUT', 'PATCH'):
            return BoardDetailWriteSerializer
        return BoardDetailReadSerializer


class TaskView(generics.CreateAPIView):
    """Create a task on a board (the requester must be a board member)."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def perform_create(self, serializer):
        """Set the creating user as the task creator."""
        serializer.save(creator=self.request.user)


class TaskAssignedToView(generics.ListAPIView):
    """List the tasks where the current user is the assignee."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        """Return tasks assigned to the current user."""
        return Task.objects.filter(assignee=self.request.user)


class TaskReviewView(generics.ListAPIView):
    """List the tasks where the current user is the reviewer."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        """Return tasks the current user reviews."""
        return Task.objects.filter(reviewer=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a single task."""

    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrOwner]


class CommentView(generics.ListCreateAPIView):
    """List a task's comments and create new ones (board members only)."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsTaskBoardMember]

    def perform_create(self, serializer):
        """Attach the comment to the URL task and the requesting author."""
        task = Task.objects.get(pk=self.kwargs['pk'])
        serializer.save(author=self.request.user, task=task)

    def get_queryset(self):
        """Return the task's comments in chronological order."""
        return Comment.objects.filter(
            task_id=self.kwargs['pk']).order_by('created_at')


class CommentDeleteView(generics.DestroyAPIView):
    """Delete a single comment (only its author may do so)."""

    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOfComment]

    def get_queryset(self):
        """Limit deletion to comments belonging to the URL task."""
        return Comment.objects.filter(task_id=self.kwargs['task_id'])
