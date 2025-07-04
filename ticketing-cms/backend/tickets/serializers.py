from rest_framework import serializers
from .models import Ticket, TicketComment
from accounts.serializers import UserSerializer
from projects.serializers import ProjectSerializer

class TicketCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = TicketComment
        fields = ['id', 'ticket', 'user', 'user_name', 'comment', 'attachment', 'is_internal', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

class TicketSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = ['id', 'ticket_id', 'title', 'description', 'project', 'project_name',
                 'created_by', 'created_by_name', 'assigned_to', 'assigned_to_name',
                 'priority', 'status', 'category', 'attachment', 'comments_count',
                 'created_at', 'updated_at', 'resolved_at', 'closed_at']
        read_only_fields = ['id', 'ticket_id', 'created_at', 'updated_at', 'created_by']
    
    def get_comments_count(self, obj):
        return obj.comments.count()

class TicketDetailSerializer(TicketSerializer):
    project = ProjectSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    comments = TicketCommentSerializer(many=True, read_only=True)

class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'project', 'priority', 'category', 'attachment']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'assigned_to', 'priority', 'status', 'category', 'attachment']
    
    def validate(self, attrs):
        # Only allow company users to assign tickets
        if 'assigned_to' in attrs:
            user = self.context['request'].user
            if not user.is_company_user:
                raise serializers.ValidationError("Only company users can assign tickets")
        
        return attrs

class TicketCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketComment
        fields = ['ticket', 'comment', 'attachment', 'is_internal']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate(self, attrs):
        # Only company users can create internal comments
        if attrs.get('is_internal', False):
            user = self.context['request'].user
            if not user.is_company_user:
                raise serializers.ValidationError("Only company users can create internal comments")
        
        return attrs