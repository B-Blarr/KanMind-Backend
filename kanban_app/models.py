from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    title = models.CharField(max_length=30)
    owner = models.ForeignKey(User, related_name='user_owned', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='member_board')

    def __str__(self):
        return self.title
    

class Task(models.Model):

    STATUS_CHOICES = [
        ('to-do' , 'to-do'),
        ('in-progress' , 'in-progress'),
        ('review' , 'review'),
        ('done' , 'done'),
    ]
    PRIORITY_CHOICES = [
        ('low' , 'low'),
        ('medium' , 'medium'),
        ('high' , 'high')
    ]

    board = models.ForeignKey(Board, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to-do')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='low')
    assignee = models.ForeignKey(User, related_name='assigned_tasks', null=True,blank=True, on_delete=models.SET_NULL)
    reviewer = models.ForeignKey(User, related_name='review_tasks', null=True, blank=True, on_delete=models.SET_NULL)
    due_date = models.DateField()
    creator = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='authored_comments', on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    task = models.ForeignKey(Task, related_name='comments' , on_delete=models.CASCADE)

    def __str__(self):
        return self.content