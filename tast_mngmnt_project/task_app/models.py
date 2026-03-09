from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    icon = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'low'),
        ('medium', 'medium'),
        ('high', 'high'),
        ('urgent', 'urgent'),
    ]

    STATUS_CHOICES = [
        ('todo', 'todo'),
        ('in_progress', 'in_progress'),
        ('completed', 'completed'),
        ('archived', 'archived'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICES, default='low')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateTimeField()
    completed_at = models.DateTimeField(null=True)
    is_important = models.BooleanField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)