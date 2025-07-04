from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Project
from .serializers import ProjectSerializer, ProjectDetailSerializer, ProjectCreateSerializer

# Create your views here.

class ProjectListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectCreateSerializer
        return ProjectSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_company_user:
            return Project.objects.filter(company=user.company, is_active=True)
        else:  # client user
            return Project.objects.filter(client=user, is_active=True)
    
    def perform_create(self, serializer):
        # Ensure company is set to user's company for company users
        if self.request.user.is_company_user:
            serializer.save(company=self.request.user.company)
        else:
            serializer.save()

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_company_user:
            return Project.objects.filter(company=user.company)
        else:  # client user
            return Project.objects.filter(client=user)
    
    def update(self, request, *args, **kwargs):
        # Only company users can update projects
        if not request.user.is_company_user:
            return Response(
                {'detail': 'Only company users can update projects.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # Only company admins can delete projects
        if request.user.user_type != 'company_admin':
            return Response(
                {'detail': 'Only company admins can delete projects.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        # Soft delete - just mark as inactive
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MyProjectsView(generics.ListAPIView):
    """Get projects assigned to current user as project manager"""
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Project.objects.filter(
            project_manager=self.request.user, 
            is_active=True
        ).order_by('-created_at')
