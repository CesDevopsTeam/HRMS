from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('Employee/', views.Employee, name='Employee'),
    path('CRUD_Employee/<int:pk>/', views.CRUD_Employee, name='CRUD_Employee'),
    path('CRUD_Employee/', views.CRUD_Employee, name='CRUD_Employee_without_pk'),


    path('Save_Personal_Info/', views.Save_Personal_Info, name='Save_Personal_Info'),
    path('Save_Job_Info/', views.Save_Job_Info, name='Save_Job_Info'),
    path('Save_Contact_Info/', views.Save_Contact_Info, name='Save_Contact_Info'),
    path('Save_Financial_Info/', views.Save_Financial_Info, name='Save_Financial_Info'),
    path('Save_Documents_Info/', views.Save_Documents_Info, name='Save_Documents_Info'),
    path('Save_Health_Info/', views.Save_Health_Info, name='Save_Health_Info'),
    path('Save_Verification_Info/', views.Save_Verification_Info, name='Save_Verification_Info'),
    path('Save_Salary_Deduction_Info/', views.Save_Salary_Deduction_Info, name='Save_Salary_Deduction_Info'),
    path('Save_Salary_Earning_Info/', views.Save_Salary_Earning_Info, name='Save_Salary_Earning_Info'),
    path('Save_Employee_Status/', views.Save_Employee_Status, name='Save_Employee_Status'),
    path('Check_Availability/', views.Check_Availability, name='Check_Availability'),
    path('ClearSession/', views.ClearSession, name='ClearSession'),






    path('MarkAttendence/', views.MarkAttendence, name='MarkAttendence'),
    path('SalarySleep/', views.SalarySleep, name='view_salary_slip'),
    path('Report/', views.Report, name='Report'),
    path('IndividualReports/<int:pk>', views.IndividualReports, name='IndividualReports'),
    path('Holidays/', views.Holidays, name='Holidays'),




    path('add_dummy_attendance/', views.add_dummy_attendance, name='add_dummy_attendance'),
    path('captch/', views.captch, name='captch'),
]