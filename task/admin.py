from django.contrib import admin

from .models import  Task, Rating
class TaskAdmin(admin.ModelAdmin):
    list_display = ('employee', 'task_description', 'assigned_at', 'is_acknowledged')
    search_fields = ('task_description',)
    list_filter = ('assigned_at', 'is_acknowledged')
    list_editable = ('is_acknowledged',)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('task', 'employee', 'rated_to', 'score', 'comment', 'created_at')  # Added rated_to
    search_fields = ('task__task_description', 'employee__emp_name', 'rated_to__emp_name')  # Added rated_to for search
    list_filter = ('score', 'rated_to')  # Added rated_to for filtering

admin.site.register(Task, TaskAdmin)
admin.site.register(Rating, RatingAdmin)