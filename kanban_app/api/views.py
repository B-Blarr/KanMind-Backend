from rest_framework import generics
from .serializers import BoardSerializer, BoardDetailReadSerializer,\
    BoardDetailWriteSerializer, TaskSerializer, TaskDetailSerializer,\
    CommentSerializer
from kanban_app.models import Board, Task, Comment
from django.db.models import Q 
from .permissions import IsOwnerOrMember, IsBoardMember, IsCreatorOrOwner
from rest_framework.permissions import IsAuthenticated


class BoardView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()
        

class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    permission_classes = [IsOwnerOrMember, IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return BoardDetailWriteSerializer
        return BoardDetailReadSerializer
    

class TaskView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBoardMember, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TaskAssignedToView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)
    

class TaskReviewView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)    
    

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrOwner]


class CommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []