from rest_framework import generics
from .serializers import BoardSerializer, BoardDetailReadSerializer,\
BoardDetailWriteSerializer
from kanban_app.models import Board
from django.db.models import Q 
from .permissions import IsOwnerForDelete
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
    permission_classes = [IsOwnerForDelete, IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return BoardDetailWriteSerializer
        return BoardDetailReadSerializer


    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()