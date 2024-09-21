from django.contrib import admin
from .models import Office, Department, Role

# Register Office model
@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('office_name', 'office_code', 'location', 'ceo', 'staff_count')
    search_fields = ('office_name', 'office_code', 'location')
    list_filter = ('location', 'ceo')
    ordering = ('office_code',)

# Register Department model
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'date')
    search_fields = ('department_name',)
    ordering = ('department_name',)

# Register Role model
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'date')
    search_fields = ('role_name',)
    ordering = ('role_name',)
