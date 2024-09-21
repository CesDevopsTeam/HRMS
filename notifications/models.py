from django.db import models
from Attendance.models import EmployeePersonalInfo
from django.utils import timezone

# Create your models here.
class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('personal', 'Personal Leave'),
        ('sick', 'Sick Leave'),
        ('vacation', 'Vacation'),
        ('casual', 'Casual Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('bereavement', 'Bereavement Leave'),
        ('public_holiday', 'Public Holiday Leave'),
        ('unpaid', 'Unpaid Leave'),
        ('medical', 'Medical Leave'),
        ('family', 'Family Leave'),
    ]

    LEAVE_DURATION_CHOICES = [
        ('half_day', 'Half Day'),
        ('full_day', 'Full Day'),
    ]

    employee = models.ForeignKey(EmployeePersonalInfo, on_delete=models.CASCADE, related_name="leave_requests")
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_duration = models.CharField(max_length=50, choices=LEAVE_DURATION_CHOICES)
    subject = models.CharField(max_length=255, blank=True, null=True)
    reason = models.TextField()
    office = models.BigIntegerField(verbose_name="Office ID", null=True, blank=True)
    department = models.BigIntegerField(verbose_name="Department ID", null=True, blank=True)
    role = models.BigIntegerField(verbose_name="Role ID", null=True, blank=True)
    supporting_document = models.FileField(upload_to='supporting_documents/', blank=True, null=True)
    leave_applied_on = models.DateTimeField(default=timezone.now, verbose_name="Leave Applied On")
    approved_on = models.DateTimeField(blank=True, null=True, verbose_name="Approved On")
    approved_by = models.ForeignKey(EmployeePersonalInfo, on_delete=models.SET_NULL, related_name="approved_leave_requests", null=True, blank=True, verbose_name="Approved By")
    is_approved = models.BooleanField(default=False, verbose_name="Is Approved")
    remark = models.TextField(blank=True, null=True, verbose_name="Remark")



    def __str__(self):
        return f"{self.employee.emp_name} - {self.leave_type} from {self.start_date} to {self.end_date}"





class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('error', 'Error'),
    ]
    
    sender = models.ForeignKey(EmployeePersonalInfo, on_delete=models.CASCADE, related_name="sent_notifications")
    recipient = models.ForeignKey(EmployeePersonalInfo, on_delete=models.CASCADE, related_name="received_notifications")
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    read_at = models.DateTimeField(null=True, blank=True)
    redirect = models.CharField(max_length=1000,null=True) 

    class Meta:
        ordering = ['-created_at']

    def mark_as_read(self):
        self.is_read = True
        self.read_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Notification from {self.sender.emp_name} to {self.recipient.emp_name} ({self.get_notification_type_display()})"
