
from django.db import models
from Attendance.models import EmployeePersonalInfo
from django.contrib.auth.models import User

class Task(models.Model):
    employee = models.ForeignKey(EmployeePersonalInfo, on_delete=models.CASCADE, related_name='tasks')
    task_title = models.CharField(max_length=255, verbose_name="Task Title", default="Untitled Task")
 
    task_description = models.TextField(verbose_name="Task Description")
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name="Assigned At")
    complete_before = models.DateField(null=True, blank=True, verbose_name="Complete Before")  
    is_acknowledged = models.BooleanField(default=False, verbose_name="Acknowledged")
    is_completed = models.BooleanField(default=False)
    assigned_by = models.ForeignKey(EmployeePersonalInfo, on_delete=models.CASCADE, related_name='assigned_tasks', null=True)

    
    document = models.FileField(upload_to='task_documents/', null=True, blank=True, verbose_name="Document")
    
    
class Rating(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='ratings')
    employee = models.ForeignKey(EmployeePersonalInfo, on_delete=models.CASCADE, related_name='ratings')  # Employee giving the rating
    rated_to = models.ForeignKey(EmployeePersonalInfo, on_delete=models.CASCADE, related_name='received_ratings', null=True)  # Allow null temporarily

    score = models.PositiveIntegerField(verbose_name="Rating Score")  # Define the range (e.g., 1-5)
    comment = models.TextField(blank=True, null=True, verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Rating Date")

    class Meta:
        unique_together = ('task', 'employee', 'rated_to')  # Ensure one rating per employee per task
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

    def __str__(self):
        return f"Rating by {self.employee} for {self.rated_to}: {self.score}"
