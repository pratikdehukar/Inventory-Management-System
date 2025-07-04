from rest_framework import serializers
from .models import Project
from accounts.serializers import UserSerializer, CompanySerializer

class ProjectSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    client_name = serializers.CharField(source='client.username', read_only=True)
    project_manager_name = serializers.CharField(source='project_manager.username', read_only=True)
    total_tickets = serializers.ReadOnlyField()
    open_tickets = serializers.ReadOnlyField()
    closed_tickets = serializers.ReadOnlyField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'company', 'company_name', 'client', 'client_name',
                 'project_manager', 'project_manager_name', 'status', 'start_date', 'end_date',
                 'budget', 'total_tickets', 'open_tickets', 'closed_tickets', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_tickets', 'open_tickets', 'closed_tickets']

class ProjectDetailSerializer(ProjectSerializer):
    company = CompanySerializer(read_only=True)
    client = UserSerializer(read_only=True)
    project_manager = UserSerializer(read_only=True)

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'company', 'client', 'project_manager', 
                 'status', 'start_date', 'end_date', 'budget']
    
    def validate(self, attrs):
        # Ensure client is actually a client user
        if attrs.get('client') and attrs['client'].user_type != 'client':
            raise serializers.ValidationError("Selected user is not a client")
        
        # Ensure project manager is company staff
        if attrs.get('project_manager') and attrs['project_manager'].user_type not in ['company_admin', 'company_staff']:
            raise serializers.ValidationError("Project manager must be company staff")
        
        return attrs