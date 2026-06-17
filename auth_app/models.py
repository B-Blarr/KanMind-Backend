"""Database models for the auth app (user profile; tutorial leftover)."""

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Optional profile data linked one-to-one to a Django user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
    