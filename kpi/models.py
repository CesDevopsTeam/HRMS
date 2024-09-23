from django.db import models
from main.models import Role

# Create your models here.


class KRA(models.Model):
    title = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='kras')  # Foreign key to Role
    description = models.TextField(blank=True)  # Optional description of the KRA
    kpi_value = models.CharField(max_length=255)  # KPI value, stored as a string
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the KRA was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the KRA was last updated
