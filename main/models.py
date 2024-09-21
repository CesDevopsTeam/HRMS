from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _

# Office Model
class Office(models.Model):
    office_name = models.CharField(max_length=100, verbose_name=_("Office Name"))
    office_code = models.CharField(max_length=10, unique=True, verbose_name=_("Office Code"))
    location = models.CharField(max_length=100, verbose_name=_("Location"))
    date_of_establishment = models.DateField(verbose_name=_("Date Of Establishment"))
    ceo = models.CharField(max_length=100, verbose_name=_("CEO"))
    staff_count = models.IntegerField(verbose_name=_("Staff Count"))
    remark = models.TextField(blank=True, null=True, verbose_name=_("Remark"))

    class Meta:
        verbose_name = _("Office")
        verbose_name_plural = _("Offices")
        ordering = ['office_code']  # Orders by office code

    def __str__(self):
        return f"{self.office_name} ({self.office_code})"

# Department Model
class Department(models.Model):
    department_name = models.CharField(max_length=100, verbose_name=_("Department Name"))
    date = models.DateField(verbose_name=_("Date"), default=timezone.now)

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

    def __str__(self):
        return self.department_name

# Role Model
class Role(models.Model):
    role_name = models.CharField(max_length=100, verbose_name=_("Role Name"))
    date = models.DateField(verbose_name=_("Date"), default=timezone.now)

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    def __str__(self):
        return self.role_name
