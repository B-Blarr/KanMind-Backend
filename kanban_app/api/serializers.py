from rest_framework import serializers
from kanban_app.models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'location']