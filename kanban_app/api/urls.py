from django.urls import path, include
from .views import BoardView, BoardDetailView, TaskView, TaskAssignedToView,\
TaskReviewView, TaskDetailView

urlpatterns = [
    path('boards/', BoardView.as_view(), name='board'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('tasks/', TaskView.as_view(), name='task'),
    path('tasks/assigned-to-me/', TaskAssignedToView.as_view(), name='task-assigned-to-me'),
    path('tasks/reviewing/', TaskReviewView.as_view(), name='task-reviewing'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    # path('tasks/<int:pk>/comments/', ),
]