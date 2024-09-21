from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('AdvanceOptions/', views.AdvanceOptions, name='AdvanceOptions'),
    path('AddOffice/', views.AddOffice, name='AddOffice'),
    path('AddDepartment/', views.AddDepartment, name='AddDepartment'),
    path('AddRoles/', views.AddRoles, name='AddRoles'),
    path('logout/', views.logout, name='logout'),
]