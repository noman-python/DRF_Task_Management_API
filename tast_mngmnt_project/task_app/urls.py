from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.ProfileListView.as_view(), name='profile'),
    path('profile/<int:pk>/', views.ProfileRUDView.as_view(), name='profile'),

    # Category
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category_detail/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<int:pk>/task/', views.CategoryTasksView.as_view(), name='category_tasks'),

    # Task
    path('task_list/', views.TaskListView.as_view(), name='task_list'),
    path('task_create/', views.TaskCreate.as_view(), name='task_create'),
    path('task_detail/<int:pk>/', views.TaskRUDView.as_view(), name='task_detail'),
    path('task_toggle/', views.TaskToggleCompleteView.as_view(), name='task_toggle'),
    path('task_archived/', views.TaskArchiveView.as_view(), name='task_archived'),
    path('task_bulk/', views.BulkCompleteTasksView.as_view(), name='task_bulk'),
    # Task Dashboard
    
]
