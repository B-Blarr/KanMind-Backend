from django.db import models

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=30)
    member_count = models.IntegerField()
    ticket_count = models.IntegerField()
    