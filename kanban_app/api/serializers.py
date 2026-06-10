from rest_framework import serializers
from kanban_app.models import Board
from django.contrib.auth.models import User


class BoardSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True, 
                                                  source='owner')
    member_count = serializers.SerializerMethodField()
    # ticket_count = 
    # tasks_to_do_count = 
    # tasks_high_prio_count = 

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'owner_id']

    def get_member_count(self, obj):
        return obj.members.count()
    

class UserSerializer(serializers.ModelSerializer):

    fullname = serializers.CharField(max_length=60, source='first_name')
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class BoardDetailReadSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True, 
                                                  source='owner')
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members']


class BoardDetailWriteSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, 
                                                 queryset=User.objects.all())
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'members']




