from django.contrib import admin

from kpi.models import KRA

# Register your models here.
@admin.register(KRA)
class KRAAdmin(admin.ModelAdmin):
    list_display = ('title', 'role', 'kpi_value', 'created_at', 'updated_at')
    search_fields = ('title', 'role__name')  # Allows searching by role name
    list_filter = ('role',)  # Filter by role in the admin panel
    ordering = ('created_at',)  # Order by creation date
