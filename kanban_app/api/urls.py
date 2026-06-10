from django.urls import path, include
from .views import BoardView, BoardDetailView

urlpatterns = [
    path('boards/', BoardView.as_view(), name='board'),
    path('boards/<int:pk/', BoardDetailView.as_view(), name='board-detail'),
]