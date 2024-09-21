from django.contrib import admin
from .models import (
    EmployeeAttendance, EmployeeLogin, EmployeePersonalInfo, EmployeeJobInfo, EmployeeContactInfo,
    EmployeeFinancialInfo, EmployeeDocuments, EmployeeHealthInfo,
    EmployeeVerification, EmployeeSalaryDeduction, EmployeeSalaryEarning,
    EmployeeAccess, Holiday
)

@admin.register(EmployeePersonalInfo)
class EmployeePersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'emp_name', 'gender', 'dob')
    search_fields = ('emp_id', 'emp_name', 'gender')
    list_filter = ('gender', 'dob')

@admin.register(EmployeeJobInfo)
class EmployeeJobInfoAdmin(admin.ModelAdmin):
    list_display = ('employee', 'doj', 'designation', 'office', 'department', 'role')
    search_fields = ('employee__emp_id', 'designation', 'office', 'department', 'role')
    list_filter = ('doj', 'designation')

@admin.register(EmployeeContactInfo)
class EmployeeContactInfoAdmin(admin.ModelAdmin):
    list_display = ('employee', 'mobile', 'email', 'work_location')
    search_fields = ('employee__emp_id', 'mobile', 'email')
    list_filter = ('work_location',)

@admin.register(EmployeeFinancialInfo)
class EmployeeFinancialInfoAdmin(admin.ModelAdmin):
    list_display = ('employee', 'bank_account_number', 'pan_number', 'aadhaar_linked_pan')
    search_fields = ('employee__emp_id', 'bank_account_number', 'pan_number')
    list_filter = ('aadhaar_linked_pan',)

@admin.register(EmployeeDocuments)
class EmployeeDocumentsAdmin(admin.ModelAdmin):
    list_display = ('employee', 'previous_employer_details', 'cibil_report', 'pcc')
    search_fields = ('employee__emp_id', 'previous_employer_details')
    list_filter = ('cibil_report', 'pcc')

@admin.register(EmployeeHealthInfo)
class EmployeeHealthInfoAdmin(admin.ModelAdmin):
    list_display = ('employee', 'blood_group', 'mental_health', 'medical_health')
    search_fields = ('employee__emp_id', 'blood_group')
    list_filter = ('blood_group',)

@admin.register(EmployeeVerification)
class EmployeeVerificationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'residential_address_verification', 'previous_employer_verification')
    search_fields = ('employee__emp_id',)
    list_filter = ('residential_address_verification', 'previous_employer_verification')

@admin.register(EmployeeSalaryDeduction)
class EmployeeSalaryDeductionAdmin(admin.ModelAdmin):
    list_display = ('employee', 'pf', 'esic', 'pt','tds')
    search_fields = ('employee__emp_id',)
    list_filter = ('pf', 'esic', 'pt', 'tds')

@admin.register(EmployeeSalaryEarning)
class EmployeeSalaryEarningAdmin(admin.ModelAdmin):
    list_display = ('employee', 'basic_salary', 'Bonus', 'HRA', 'travel_claim_allowed', 'overtime_allowance')
    search_fields = ('employee__emp_id', 'basic_salary')
    list_filter = ('Bonus', 'HRA', 'travel_claim_allowed')

@admin.register(EmployeeAccess)
class EmployeeAccessAdmin(admin.ModelAdmin):
    list_display = ('employee', 'advance_salary_allowed', 'offer_letter_allowed', 'payslip_allowed', 'experience_letter_allowed')
    search_fields = ('employee__emp_id',)
    list_filter = ('advance_salary_allowed', 'offer_letter_allowed', 'payslip_allowed', 'experience_letter_allowed')
@admin.register(EmployeeLogin)
class EmployeeLoginAdmin(admin.ModelAdmin):
    list_display = ('employee', 'username', 'password')
    search_fields = ('employee__emp_id', 'username')

@admin.register(EmployeeAttendance)
class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'hours_worked', 'overtime_hours', 'status', 'remark')
    list_filter = ('date', 'status')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__employee_id', 'date')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # If an object is being edited
            return self.readonly_fields + ('employee', 'date')
        return self.readonly_fields
    

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('date', 'reason', 'type')
    list_filter = ('type',)
    search_fields = ('date', 'reason')
    ordering = ('date',)

    # Optional: To make the form more user-friendly in the admin interface
    fieldsets = (
        (None, {
            'fields': ('date', 'reason', 'type')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('date', 'reason', 'type')
        }),
    )

