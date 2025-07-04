from django.urls import path
from . import views

urlpatterns = [
    # Projects
    path('', views.ProjectListCreateView.as_view(), name='project-list-create'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('my-projects/', views.MyProjectsView.as_view(), name='my-projects'),
]