from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    title = models.CharField(max_length=30)
    owner = models.ForeignKey(User, related_name='user_owned', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='member_board')

    def __str__(self):
        return self.title