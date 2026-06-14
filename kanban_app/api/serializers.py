from rest_framework import serializers
from kanban_app.models import Board, Task, Comment
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
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'member_count', 'ticket_count', 'tasks_to_do_count','tasks_high_prio_count', 'owner_id']

    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_ticket_count(self, obj):
        return obj.tasks.count()
    
    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()


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
    # comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',
                  'assignee', 'assignee_id', 'reviewer', 'reviewer_id', 
                  'due_date' ]
        
    # def get_comments_count(self, obj):
    #     return obj.tasks.comments.count()


class TaskDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=30)
    description = serializers.CharField(max_length=200)
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), 
                 source='assignee', write_only=True, required=False)
    reviewer = UserSerializer(read_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), 
                source='reviewer', write_only=True, required=False)
    due_date = serializers.DateField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority',
                  'assignee', 'assignee_id', 'reviewer', 'reviewer_id', 'due_date' ]
        

class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    author = serializers.CharField(source='author.first_name', read_only=True)
    content = serializers.CharField(max_length=200)   

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']