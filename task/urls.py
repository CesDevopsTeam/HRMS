from django.contrib import admin
from django.urls import path,include
from .views import daily_task_view, task_assign_view, assign_task_view
from . import views

urlpatterns = [
    path('', views.daily_task_view, name='daily_task'),
    path('task/', views.task, name='task'),
    
    path('assign-task/', assign_task_view, name='assign_task'),
    path('mark_task_completed/<int:task_id>/', views.mark_task_completed, name='mark_task_completed'),
    path('completed_tasks/', views.completed_tasks_view, name='completed_tasks'),
    path('acknowledge_task/<int:task_id>/', views.acknowledge_task_view, name='acknowledge_task'),
    path('navbar/',views.navbar,name= 'navbar' ),
    path('overdue-tasks/', views.overdue_tasks_view, name='overdue_tasks'),
    path('task/assigned-tasks/', views.assigned_tasks_view, name='assigned_tasks'),
    path('submit_rating/<int:task_id>/', views.submit_rating, name='submit_rating'),
    path('tasks-with-ratings/', views.tasks_with_ratings_view, name='tasks_with_ratings'),
    
    
    
    
    
   
    
    
   
    
   
    

    
    
]