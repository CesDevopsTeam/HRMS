from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

# Model for Employee Personal Information
class EmployeePersonalInfo(models.Model):
    emp_id = models.CharField(max_length=20, unique=True, verbose_name="Employee ID")
    emp_name = models.CharField(max_length=100, verbose_name="Employee Name",null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], verbose_name="Gender",null=True)
    dob = models.DateField(verbose_name="Date of Birth",null=True)
    photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True, verbose_name="Employee Photo")

# Model for Employee Job Information
class EmployeeJobInfo(models.Model):
    employee = models.OneToOneField(EmployeePersonalInfo, on_delete=models.CASCADE, related_name="job_info")
    doj = models.DateField(verbose_name="Date of Joining",null=True)
    designation = models.CharField(max_length=100, verbose_name="Designation")
    office = models.BigIntegerField(verbose_name="Office ID", null=True, blank=True)
    department = models.BigIntegerField(verbose_name="Department ID", null=True, blank=True)
    role = models.BigIntegerField(verbose_name="Role ID", null=True, blank=True)
    qualifications = models.CharField(max_length=200, verbose_name="Qualifications")
    skills = models.TextField(blank=True, null=True, verbose_name="Skills")
    certifications = models.TextField(blank=True, null=True, verbose_name="Certifications")
    achievements = models.TextField(blank=True, null=True, verbose_name="Achievements")

# Model for Employee Contact Information
class EmployeeContactInfo(models.Model):
    employee = models.OneToOneField(EmployeePersonalInfo, on_delete=models.CASCADE, related_name="contact_info")
    mobile = models.CharField(max_length=15, verbose_name="Mobile Number")
    whatsapp = models.CharField(max_length=15, verbose_name="whatsapp Number", null=True)
    email = models.EmailField(verbose_name="Email")
    residential_address = models.TextField(verbose_name="Residential Address")
    work_location = models.CharField(max_length=100, verbose_name="Work Location")
    emergency_contact_name = models.CharField(max_length=100, verbose_name="Emergency Contact Name")
    emergency_contact_phone = models.CharField(max_length=15, verbose_name="Emergency Contact Phone")
    family_contact_details = models.TextField(verbose_name="Family Contact Details")

class EmployeeFinancialInfo(models.Model):
    employee = models.OneToOneField(EmployeePersonalInfo, on_delete=models.CASCADE, related_name="financial_info")
    bank_account_number = models.CharField(max_length=20, verbose_name="Bank Account Number")
    pan_number = models.CharField(max_length=10, verbose_name="PAN Number")
    aadhaar_number = models.CharField(max_length=10, verbose_name="Aadhaar Number",null=True)
    aadhaar_linked_pan = models.BooleanField(default=False, verbose_name="Aadhaar Linked with PAN")

# Model for Employee Documents
class EmployeeDocuments(models.Model):
    employee = models.OneToOneField(EmployeePersonalInfo, on_delete=models.CASCADE, related_name="documents")
    previous_employer_details = models.TextField(verbose_name="Previous Employer Details")
    previous_employer_contact_mobile = models.CharField(max_length=15, verbose_name="Previous Employer Contact Mobile")
    previous_employer_contact_email = models.EmailField(verbose_name="Previous Employer Contact Email")
    cibil_report = models.FileField(upload_to='cibil_reports/', blank=True, null=True, verbose_name="CIBIL Report")
    pcc = models.FileField(upload_to='pcc/', blank=True, null=True, verbose_name="Police Clearance Certificate")

# Model for Employee Health Information
class EmployeeHealthInfo(models.Model):
    employee = models.OneToOneField(EmployeePersonalInfo, on_delete=models.CASCADE, related_name="health_info")
    blood_group = models.CharField(max_length=3, verbose_name="Blood Group")
    mental_health = models.TextField(blank=True, null=True, verbose_name="Mental Health")
    medical_health = models.TextField(blank=True, null=True, verbose_name="Medical Health")

# Model for Employee Verification Status
class EmployeeVerification(models.Model):
    employee = models.OneToOneField(EmployeePersonalInfo, on_delete=models.CASCADE, related_name="verification")
    residential_address_verification = models.BooleanField(default=False, verbose_name="Residential Address Verification Done")
    previous_employer_verification = models.BooleanField(default=False, verbose_name="Previous Employer Verification Done")
    residential_address_gps = models.CharField(max_length=100, blank=True, null=True, verbose_name="Residential Address GPS Location")


# Model for Employee Salary Information
class EmployeeSalaryDeduction(models.Model):
    employee = models.OneToOneField(EmployeePersonalInfo, on_delete=models.CASCADE, related_name="EmployeeSalaryDeduction")
    # Term1
    pf = models.BooleanField(default=False, verbose_name="PF Deducted")
    esic = models.BooleanField(default=False, verbose_name="ESIC Deducted")
    pt = models.BooleanField(default=False, verbose_name="PT Deducted")
    lwf = models.BooleanField(default=False, verbose_name="lwf Deducted")

    BSCD = models.CharField(max_length=255, verbose_name="BSCD",null=True)
    employee_lwf_AMT = models.CharField(max_length=255, verbose_name="employee_lwf_AMT",null=True)
    employers_lwf_AMT = models.CharField(max_length=255, verbose_name="employers_lwf_AMT",null=True)
    # Term2
    tds = models.BooleanField(default=False, verbose_name="TDS Deducted")

class EmployeeSalaryEarning(models.Model):
    employee = models.OneToOneField(EmployeePersonalInfo, on_delete=models.CASCADE, related_name="EmployeeSalaryEarning")
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="basic_salary", null=True)
    da = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="da", null=True)
    Bonus = models.BooleanField(default=False, verbose_name="Bonus Addition")
    HRA = models.BooleanField(default=False, verbose_name="HRA Addition")
    travel_claim_allowed = models.BooleanField(default=False, verbose_name="Travel Claim Allowed")
    overtime_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Overtime Allowance")
class EmployeeStatus(models.Model):
    employee = models.OneToOneField(EmployeePersonalInfo, on_delete=models.CASCADE, related_name="status")
    employment_status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    notice_period = models.BooleanField(default=False)
    resigned = models.BooleanField(default=False)
    terminated = models.BooleanField(default=False)
    dead = models.BooleanField(default=False)
    training_period = models.BooleanField(default=False)


class EmployeeLogin(models.Model):
    employee = models.OneToOneField(EmployeePersonalInfo, on_delete=models.CASCADE, related_name="Login")
    username = models.CharField(max_length=200,null=True)
    password = models.CharField(max_length=200)


class EmployeeAttendance(models.Model):
    ATTENDANCE_STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('H', 'Half Day'),
    ]

    employee = models.ForeignKey(EmployeePersonalInfo, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField(default=timezone.now)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    check_in_location = models.CharField(max_length=255, null=True, blank=True)
    check_out_location = models.CharField(max_length=255, null=True, blank=True)
    hours_worked = models.CharField(max_length=5, null=True, blank=True)  # Store as HH:MM format
    overtime_hours = models.CharField(max_length=5, null=True, blank=True)  # Store overtime as HH:MM
    reason_for_absence = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=ATTENDANCE_STATUS_CHOICES, default='A')
    remark = models.CharField(max_length=50, null=True, blank=True)
    remark_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'date')  # Ensure unique attendance per employee per day

    def __str__(self):
        return f"Attendance for {self.employee} on {self.date}"
    
    def save(self, *args, **kwargs):
        now = timezone.localtime(timezone.now())
        
        # if not self.check_in:
        #     self.check_in = now.time()  # Save current time as check_in if not set
        
        # if not self.check_out:
        #     self.check_out = now.time()  # Save current time as check_out if not set
        if not self.check_in:
            self.check_in = None  # Set current time as check_in if not provided
        
        # Do not auto-fill check_out unless explicitly provided
        if not self.check_out:
            self.check_out = None  # Keep check_out as None unless manually set

        
        # Calculate hours_worked and overtime_hours if check_in and check_out are both present
        if self.check_in and self.check_out:
            check_in_datetime = datetime.combine(self.date, self.check_in)
            check_out_datetime = datetime.combine(self.date, self.check_out)
            
            if check_out_datetime < check_in_datetime:
                # Handle cases where check_out is past midnight
                check_out_datetime += timedelta(days=1)
                
            delta = check_out_datetime - check_in_datetime
            
            # Convert total working time into HH:MM format
            total_seconds = delta.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            self.hours_worked = f"{hours:02}:{minutes:02}"  # Store as HH:MM format
            
            # Calculate overtime and status based on hours_worked
            if hours >= 8:
                overtime_seconds = (total_seconds - 8 * 3600)  # Subtract 8 hours from total
                overtime_hours = int(overtime_seconds // 3600)
                overtime_minutes = int((overtime_seconds % 3600) // 60)
                self.overtime_hours = f"{overtime_hours:02}:{overtime_minutes:02}"
                
                self.status = 'P'
                self.remark = 'Present'
                self.remark_reason = 'Worked 8 hours or more'
            elif 7.5 <= (hours + minutes / 60) < 8:
                self.overtime_hours = "00:00"  # No overtime
                self.status = 'P'
                self.remark = 'Late'
                self.remark_reason = 'Worked slightly less than 8 hours'
            elif 4 < (hours + minutes / 60) <= 7.5:
                self.overtime_hours = "00:00"  # No overtime
                self.status = 'H'
                self.remark = 'Half Day'
                self.remark_reason = 'Worked between 4 and 7.5 hours'
            else:
                self.overtime_hours = "00:00"
                self.status = 'A'
                self.remark = 'Absent'
                self.remark_reason = 'Worked less than 4 hours'
        else:
            self.hours_worked = "00:00"
            self.overtime_hours = "00:00"
            self.status = 'A'
            self.remark = 'Absent'
            self.remark_reason = 'No check-in or check-out time recorded'
        
        super().save(*args, **kwargs)


        
class Holiday(models.Model):
    FULL_DAY = 'FD'
    HALF_DAY = 'HD'
    HOLIDAY_CHOICES = [
        (FULL_DAY, 'Full Day'),
        (HALF_DAY, 'Half Day'),
    ]
    
    date = models.DateField(help_text="Date of the holiday")
    reason = models.CharField(max_length=255, help_text="Reason for the holiday")
    type = models.CharField(
        max_length=2,
        choices=HOLIDAY_CHOICES,
        default=FULL_DAY,
        help_text="Type of the holiday (Full Day or Half Day)"
    )
    
    class Meta:
        ordering = ['date']
        verbose_name = 'Holiday'
        verbose_name_plural = 'Holidays'
    
    def __str__(self):
        return f"{self.date} - {self.reason} ({self.get_type_display()})"

class EmployeeAccess(models.Model):
    employee = models.OneToOneField(EmployeePersonalInfo, on_delete=models.CASCADE, related_name="EmployeeAccess")
    advance_salary_allowed = models.BooleanField(default=False, verbose_name="Advance Salary Allowed")
    offer_letter_allowed = models.BooleanField(default=True, verbose_name="Offer Letter Allowed")
    payslip_allowed = models.BooleanField(default=True, verbose_name="Payslip Allowed")
    experience_letter_allowed = models.BooleanField(default=False, verbose_name="Experience/Relieving Letter Allowed")
    
    
    


