from rest_framework import serializers
from kanban_app.models import Board, Task
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    fullname = serializers.CharField(max_length=60, source='first_name')
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class BoardSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True, 
                                                  source='owner')
    member_count = serializers.SerializerMethodField()
    members = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=User.objects.all())
    # ticket_count = 
    # tasks_to_do_count = 
    # tasks_high_prio_count = 

    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'member_count', 'owner_id']

    def get_member_count(self, obj):
        return obj.members.count()
    

class BoardDetailReadSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True, 
                                                  source='owner')
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members']


class BoardDetailWriteSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, 
                                                 queryset=User.objects.all(), write_only=True)
    owner_data = UserSerializer(source='owner', read_only=True)
    members_data = UserSerializer(source='members', many=True, read_only=True)
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'owner_data', 'members_data', ]


class TaskSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    title = serializers.CharField(max_length=30)
    description = serializers.CharField(max_length=200)
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), 
                 source='assignee', write_only=True, required=False)
    reviewer = UserSerializer( read_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), 
                source='reviewer', write_only=True, required=False)
    due_date = serializers.DateField()
    # comments_count fehlt noch

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',
                  'assignee', 'assignee_id', 'reviewer', 'reviewer_id', 
                  'due_date', ]