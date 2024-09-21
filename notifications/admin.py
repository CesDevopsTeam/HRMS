from django.contrib import admin

from notifications.models import LeaveRequest, Notification

# Register your models here.
@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'leave_duration', 'subject', 'reason', 'office', 'department', 'role')
    list_filter = ('leave_type', 'leave_duration', 'start_date', 'end_date')
    search_fields = ('employee__emp_name', 'subject', 'reason')
    readonly_fields = ('employee', 'start_date', 'end_date')  # Make these fields read-only in admin

    def has_change_permission(self, request, obj=None):
        # Add custom permissions or logic if needed
        return super().has_change_permission(request, obj)
    


class NotificationAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('id', 'sender', 'recipient', 'message', 'notification_type', 'created_at', 'is_read')
    
    # Add search functionality for these fields
    search_fields = ('sender__emp_name', 'recipient__emp_name', 'message')
    
    # Add filters for these fields
    list_filter = ('notification_type', 'is_read', 'created_at')
    
    # Define the fields to be read-only in the admin form
    readonly_fields = ('created_at', 'read_at')

    # Ordering by created_at in descending order to show the latest notifications first
    ordering = ('-created_at',)

# Register the Notification model with the custom admin options
admin.site.register(Notification, NotificationAdmin)

