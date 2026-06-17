from django.urls import path, include
from .views import BoardView, BoardDetailView, TaskView, TaskAssignedToView,\
TaskReviewView, TaskDetailView, CommentView, CommentDeleteView

urlpatterns = [
    path('boards/', BoardView.as_view(), name='board'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('tasks/', TaskView.as_view(), name='task'),
    path('tasks/assigned-to-me/', TaskAssignedToView.as_view(),\
          name='task-assigned-to-me'),
    path('tasks/reviewing/', TaskReviewView.as_view(), name='task-reviewing'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/comments/', CommentView.as_view(), name='comment'),
    path('tasks/<int:task_id>/comments/<int:pk>/', CommentDeleteView.as_view(),\
          name='comment-delete'),
]