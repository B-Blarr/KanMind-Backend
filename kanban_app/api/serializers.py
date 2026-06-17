"""Serializers for the kanban app: boards, tasks and comments."""

from rest_framework import serializers
from kanban_app.models import Board, Task, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Compact user representation (id, email, full name)."""

    fullname = serializers.CharField(max_length=60, source='first_name')
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class BoardSerializer(serializers.ModelSerializer):
    """Board summary for list/create with task counts and owner id."""

    owner_id = serializers.PrimaryKeyRelatedField(
        read_only=True, source='owner')
    member_count = serializers.SerializerMethodField()
    members = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=User.objects.all())
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'member_count', 'ticket_count',
                  'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']

    def get_member_count(self, obj):
        """Return how many members the board has."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Return the total number of tasks on the board."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Return the number of tasks still in the 'to-do' status."""
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        """Return the number of tasks with 'high' priority."""
        return obj.tasks.filter(priority='high').count()


class TaskSerializer(serializers.ModelSerializer):
    """Full task representation for create and list endpoints."""

    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    title = serializers.CharField(max_length=30)
    description = serializers.CharField(max_length=200)
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assignee',
        write_only=True, required=False)
    reviewer = UserSerializer(read_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='reviewer',
        write_only=True, required=False)
    due_date = serializers.DateField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',
                  'assignee', 'assignee_id', 'reviewer', 'reviewer_id',
                  'due_date', 'comments_count']

    def get_comments_count(self, obj):
        """Return the number of comments on the task."""
        return obj.comments.count()

    def validate(self, attrs):
        """Ensure the chosen assignee and reviewer are members of the board."""
        board = attrs.get('board')
        assignee = attrs.get('assignee')
        reviewer = attrs.get('reviewer')
        members = board.members.all()
        if assignee and assignee not in members:
            raise serializers.ValidationError(
                {'assignee_id': 'Assignee muss Mitglied des Boards sein.'})
        if reviewer and reviewer not in members:
            raise serializers.ValidationError(
                {'reviewer_id': 'Reviewer muss Mitglied des Boards sein.'})
        return attrs


class BoardDetailReadSerializer(serializers.ModelSerializer):
    """Board detail for GET: owner id, members and the nested task list."""

    owner_id = serializers.PrimaryKeyRelatedField(
        read_only=True, source='owner')
    members = UserSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class BoardDetailWriteSerializer(serializers.ModelSerializer):
    """Board detail for PATCH: writable members, returns owner/members data."""

    members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True)
    owner_data = UserSerializer(source='owner', read_only=True)
    members_data = UserSerializer(source='members', many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'owner_data', 'members_data']


class TaskDetailSerializer(serializers.ModelSerializer):
    """Task representation for update/delete; board is immutable (excluded)."""

    title = serializers.CharField(max_length=30)
    description = serializers.CharField(max_length=200)
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assignee',
        write_only=True, required=False)
    reviewer = UserSerializer(read_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='reviewer',
        write_only=True, required=False)
    due_date = serializers.DateField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority',
                  'assignee', 'assignee_id', 'reviewer', 'reviewer_id',
                  'due_date']

    def validate(self, attrs):
        """Ensure assignee and reviewer are members of the task's board."""
        board = self.instance.board
        assignee = attrs.get('assignee')
        reviewer = attrs.get('reviewer')
        members = board.members.all()
        if assignee and assignee not in members:
            raise serializers.ValidationError(
                {'assignee_id': 'Assignee muss Mitglied des Boards sein.'})
        if reviewer and reviewer not in members:
            raise serializers.ValidationError(
                {'reviewer_id': 'Reviewer muss Mitglied des Boards sein.'})
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """Comment representation; the author is shown as the user's full name."""

    created_at = serializers.DateTimeField(read_only=True)
    author = serializers.CharField(source='author.first_name', read_only=True)
    content = serializers.CharField(max_length=200)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
