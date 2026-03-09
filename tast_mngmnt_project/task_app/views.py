from django.shortcuts import render
from .models import Category, Task
from .Api.serializers import CategorySerializer, TaskSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework import generics
from .Api.permissions import UserProfileReadPermission, CategoryPermissions, TaskPermissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import filters
from django.utils import timezone
from django.db.models import Count, Q


# Create your views here.
class ProfileListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

class ProfileRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, UserProfileReadPermission]
    queryset = User.objects.all()
    serializer_class = ProfileSerializer


# Category Views
class CategoryListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [CategoryPermissions]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryTasksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, CategoryPermissions]
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority']

    def get_queryset(self, request, pk, *args, **kwargs):
        cat = Category.objects.get(pk=pk)
        tasks = Task.objects.filter(user=self.request.user, category=cat)
        serializer = TaskSerializer(tasks, many=True)

        return Response({
            'count': tasks.count(),
            'tasks': serializer.data
        })
    

# Task View
class TaskListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        today = timezone.now().date()
        queryset = Task.objects.filter(
            user=self.request.user,
            status__in=['todo', 'in_progress', 'completed', 'archived'],
            priority__in=['low', 'medium', 'high', 'urgent'],
            category=pk,
            is_important=True,
            due_date=today
        ).order_by('-created_at', 'due_date', 'priority', '-updated_at')
        return queryset


class TaskCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, TaskPermissions]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskToggleCompleteView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, TaskPermissions]
    def toggle_task(request, pk):
        task = Task.objects.get(pk=pk)
        if task.status == "todo":
            task.status = "completed"
            task.completed_at = timezone
        else:
            task.status = "todo"
            task.completed_at = None
        task.save()
        return Response({"message":"task updated", "status":task.status} )

class TaskArchiveView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, TaskPermissions]
    serializer_class = TaskSerializer
    def task_archived(request, pk):
        task = Task.objects.get(pk=pk)
        if task.status != "archived":
            task.status = "archived"
            task.save()
            return Response({"message":"task in archived"})
        else:
            return Response({"message": "task already in archived"})

class BulkCompleteTasksView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, TaskPermissions]
    def post(self, request, *args, **kwargs):
        task_ids = Task.objects.get("task_ids", [])
        if not task_ids:
            return Response({"message": "no task ids provided"})
        
        tasks = Task.objects.filter(id__in=task_ids, user=request.user)

        for task in tasks:
            task.status = "completed"
            task.completed_at = timezone.now()
            task.save()
        
        count = tasks.count()
        return Response({"message": f"{count} task completed successfully"})
    
class TaskStatisticsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    def get_total_tasks(self):
        pk = self.kwargs['pk']
        tasks = Task.objects.filter(pk=pk, user=self.request.user)
        count = tasks.count()
        return Response({"message": f"{count}"})
    
    def get_status_tasks(self):
        counts = Task.objects.aggregate(
            total_todo = Count('id', filter=Q(status='todo')),
            total_in_progress = Count('id', filter=Q(status='in_progress')),
            total_completed = Count('id', filter=Q(status='completed')),
            total_archived = Count('id', filter=Q(status='archived')),
            total_all = Count('id')
        )
        return counts
    
    def get_completed_today(self):
        today = timezone.now().date()
        task = Task.objects.filter(status="completed", completed_at__date=today).count()
        return task
    
    def get_overdue_tasks(self):
        today = timezone.now()
        overdue = Task.objects.filter(status=["todo", "in_progress"], due_date__It=today).count()
        return overdue
    
    def get_priority_tasks(self):
        priorities = Task.objects.filter(priority=["high", "urgent"]).count()
        return priorities
    
    def calculate_completion_rate(self, total, completed):
        per = (completed / total) * 100
        return per
    
    def get(self):
        total = self.get_total_tasks()
        status = self.get_status_tasks()
        complete_today = self.get_completed_today()
        overdue = self.get_overdue_tasks()
        priority = self.get_priority_tasks()

        completed_tasks = status.get('completed', 0)
        completed_rate = self.calculate_completion_rate(total, completed_tasks)

        statistics = {
            "total_tasks": total,
            "total_status_tasks": status,
            "total completed_today":complete_today,
            "total_overdue":overdue,
            "total_priority(urgent/high)":priority,
            "completion_rate":completed_rate
        }

        return statistics

class OverdueTasksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    def overdue_task(self, pk):
        today = timezone.now()
        overdue_tasks = Task.objects.filter(
           due_date__It=today,
           status__ne='completed',
           user=self.request.user
           ).order_by('due_date')
        return overdue_tasks
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "overdue_task": serializer.data
        })

class TodayTasksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self, request, *args, **kwargs):
        today = timezone.now().date()
        return Task.objects.filter(
            due_date=today,
            user=self.request.user
        ).exclude(
            status='archived'
        ).order_by('priority')