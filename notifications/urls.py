from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.Notifications, name='Notifications'),
    path('send_notification/', views.send_notification, name='send_notification'),
    path('mark-read/<int:pk>/', views.mark_notification_as_read, name='mark_read'),
    path('leave/', views.leave, name='leave'),
    path('leave_Approve/', views.leave_approve, name='leave_approve'),

    
]