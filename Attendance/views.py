import calendar
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from Attendance.models import EmployeeAttendance, EmployeeContactInfo, EmployeeDocuments, EmployeeFinancialInfo, EmployeeHealthInfo, EmployeeJobInfo, EmployeeLogin, EmployeePersonalInfo, EmployeeSalaryDeduction, EmployeeSalaryEarning, EmployeeStatus, EmployeeVerification, Holiday
from Attendance.utils import get_date_range
from main.models import Department, Office, Role
from main.utils import Validate_Role, calculate_attendance_and_salary, get_Salary_Calculations, userInfo  # Import the messages module
def dashboard(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    
    # Get the start and end date from the request (GET parameters)
    start_date_str = request.GET.get('from_date')
    end_date_str = request.GET.get('end_date')
    # Parse the start and end dates or get default date range
    if start_date_str and end_date_str:
        try:
            start_date_str=f"{start_date_str}-15"
            end_date_str=f"{end_date_str}-15"
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            start_date, end_date = get_date_range()  # Default date range handling
    else:
        start_date, end_date = get_date_range()

    MSG = None
    Time = None
    My_Id = request.session['My_Id']  # Assuming employee ID is stored in session
    current_date = timezone.localtime(timezone.now()).date()

    # Get employee and today's attendance
    try:
        employee_personal_info = EmployeePersonalInfo.objects.get(emp_id=My_Id)
        try:
            attendance = EmployeeAttendance.objects.get(employee=employee_personal_info, date=current_date)
        except EmployeeAttendance.DoesNotExist:
            attendance = EmployeeAttendance(employee=employee_personal_info, date=current_date)
        if attendance.check_in and not attendance.check_out:
            Time = f"Check-In Time: {attendance.check_in}"
            MSG = "Check-Out"
        elif attendance.check_in and attendance.check_out:
            Time = f"Total Working: {attendance.hours_worked} Hr"
            MSG = None
        else:
            attendance.check_in = timezone.localtime(timezone.now()).time()
            Time = "00:00:00"
            MSG = "Check-In"
    except EmployeePersonalInfo.DoesNotExist:
        pass

    #<============ Start Attendance Data code ==============>
    today = timezone.now().date()
    
    # Filter attendance records for the custom date range
    Attendance_Report = EmployeeAttendance.objects.filter(
        employee=employee_personal_info,
        date__range=(start_date, end_date)
    )

    employee_data = userInfo(My_Id)

    #<============ End Attendance Data code ==============>





    #<============ Start Report Code ==============>
    # Calculate total days in the custom date range
    total_days_range = (end_date - start_date).days + 1

    Weekly_Off_days = 0
    sundays = []
    Total_Holidays = 0

    # Loop through each day in the date range to count Sundays and holidays
    for day_offset in range(total_days_range):
        current_date = start_date + timedelta(days=day_offset)
        if current_date.weekday() == 6:  # Sunday
            sundays.append(current_date)
            Weekly_Off_days += 1

    # Query holidays for the custom date range
    holidays = Holiday.objects.filter(
        date__range=(start_date, end_date)
    )
    filtered_holidays = holidays.exclude(date__in=sundays)
    Total_Holidays = filtered_holidays.count()

    # Get employee details and attendance for report
    emp = EmployeePersonalInfo.objects.get(emp_id=request.session['My_Id'])
    employee_data = userInfo(emp.emp_id)

    # Call helper function to calculate attendance and salary details
    calculation_data = calculate_attendance_and_salary(
        emp,
        start_date,  # Use start_date for the year context
        end_date,  # Use start_date for the month context (if needed)
        total_days_range,
        Weekly_Off_days,
        Total_Holidays,
        sundays
    )
    

    

    try:
        Basic_Salary, Dearness_Allowence, In_Hand = get_Salary_Calculations(emp, calculation_data["Payable_Days"], total_days_range)
    except:
        Basic_Salary = Dearness_Allowence = In_Hand = None
    # Prepare the data for the template
    data = [{
        "Payable_Days": calculation_data["Payable_Days"],
        "Working_Days": calculation_data["Working_Days"],
        "Present_days_count": calculation_data["Present_days_count"],
        "Total_days": total_days_range,
        "Weekly_Off_days": Weekly_Off_days,
        "sundays": sundays,
        "Total_Holidays": Total_Holidays,
        "employee_details": employee_data,
        "Full_days": calculation_data["Full_days"],
        "Half_days": calculation_data["Half_days"],
        "Late_Mark_days": calculation_data["Late_Mark_days"],
        "leave": calculation_data["leave"],
        "Basic_Salary": Basic_Salary,
        "Dearness_Allowence": Dearness_Allowence,
        "In_Hand": In_Hand,
    }]

    #<============ End Report Code ==============>










    #<============ Start Reporties Code ==============>
    Reporties = []
    today_date = date.today()

    my_id = request.session.get('My_Id')  # Safely retrieve session ID

    # Get the employee's personal information
    try:
        personal_info = EmployeePersonalInfo.objects.get(emp_id=my_id)
    except EmployeePersonalInfo.DoesNotExist:
        return None  # You might want to return an appropriate error or redirect here

    # Get the employee's job information
    try:
        job_info = EmployeeJobInfo.objects.get(employee=personal_info)
    except EmployeeJobInfo.DoesNotExist:
        job_info = None

    # Get the employee's role information
    role_info = Role.objects.filter(pk=job_info.role).first() if job_info else None

    # Check if the employee is a Project Manager
    if role_info and role_info.role_name.strip().lower() == "project manager":
        try:
            # Get all employees in the same office and department
            attendies = EmployeeJobInfo.objects.filter(office=job_info.office, department=job_info.department)
        except EmployeeJobInfo.DoesNotExist:
            attendies = None

        if attendies:
            # Fetch all attendances for today in one query
            attendances_today = EmployeeAttendance.objects.filter(date=today_date, employee__in=[a.employee for a in attendies])
            
            # Loop through attendies and build the Reporties list
            for attendee in attendies:
                attendance = attendances_today.filter(employee=attendee.employee).first()  # Get attendance for each attendee
                if attendance:
                    # Get personal info for the attendee
                    user_details = EmployeePersonalInfo.objects.get(emp_id=attendee.employee.emp_id)
                    
                    Reporties.append({
                        'Personal_Info': user_details,
                        'Attendance': attendance
                    })
    print(Reporties)

#<============ End Reporties Code ==============>


    # Prepare the context for rendering the template
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'data': data,
        'employee_data': employee_data,
        "Time": Time,
        "Attendance_Report": Attendance_Report,
        "MSG": MSG,
        "Reporties":Reporties,
    }
    
    return render(request, "Attendence_Dashboard.html", context)


















def SalarySleep(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    month = request.GET.get('month')
    year = request.GET.get('year')
    if month and year:
        messages.success(request,"Filter Applied")

    

    employee_data = userInfo(request.session['My_Id'])
    print(employee_data)
    context={
        'employee_data':employee_data,
    }
    return render(request,"SalarySleep.html",context)






def Employee(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')
    today = timezone.now().date()
    birthdays = EmployeePersonalInfo.objects.filter(
        dob__month=today.month,
        dob__day=today.day
    )
    employee_list = EmployeePersonalInfo.objects.all()
    paginator = Paginator(employee_list, 2)  # Show 2 employees per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    
    context={
        'Employee':page_obj,
        'birthdays': birthdays,
    }
    return render(request,"Employee.html",context)


def CRUD_Employee(request, pk=None):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    employee_list = EmployeePersonalInfo.objects.all()
    Office_Model = Office.objects.all()
    Department_Model = Department.objects.all()
    Role_Model = Role.objects.all()
    EmpPersonalInfo = None
    EmployeeJobInfo_model = None
    EmployeeContactInfo_model = None
    EmployeeFinancialInfo_model = None
    EmployeeDocuments_model = None
    EmployeeHealthInfo_model = None
    EmployeeVerification_model = None
    EmployeeSalaryDeduction_model = None
    EmployeeSalaryEarning_model = None
    EmployeeStatus_model=None
    EmployeeLogin_model=None
    if pk:
        try:
            EmpPersonalInfo_Model=EmployeePersonalInfo.objects.get(pk=pk)
            request.session['emp_id'] = EmpPersonalInfo_Model.emp_id
        except:        
            if 'emp_id' in request.session:
                del request.session['emp_id']
            messages.error(request,"Oops! Something Wrong")

    else:
        pass

    if 'emp_id' in request.session:

        emp_id=request.session['emp_id']
        try:
            EmpPersonalInfo = EmployeePersonalInfo.objects.get(emp_id=emp_id)
        except:
            EmpPersonalInfo = None
        try:
            employee_personal_info = EmployeePersonalInfo.objects.get(emp_id=emp_id)
            EmployeeJobInfo_model = EmployeeJobInfo.objects.get(employee=employee_personal_info)
        except:
            EmployeeJobInfo_model=None
        try:
            employee_personal_info = EmployeePersonalInfo.objects.get(emp_id=emp_id)
            EmployeeContactInfo_model = EmployeeContactInfo.objects.get(employee=employee_personal_info)
        except:
            EmployeeContactInfo_model=None
        try:
            employee_personal_info = EmployeePersonalInfo.objects.get(emp_id=emp_id)
            EmployeeFinancialInfo_model = EmployeeFinancialInfo.objects.get(employee=employee_personal_info)
        except:
            EmployeeFinancialInfo_model=None
        try:
            employee_personal_info = EmployeePersonalInfo.objects.get(emp_id=emp_id)
            EmployeeDocuments_model = EmployeeDocuments.objects.get(employee=employee_personal_info)
        except:
            EmployeeDocuments_model=None
        try:
            employee_personal_info = EmployeePersonalInfo.objects.get(emp_id=emp_id)
            EmployeeHealthInfo_model = EmployeeHealthInfo.objects.get(employee=employee_personal_info)
        except:
            EmployeeHealthInfo_model=None
        try:
            employee_personal_info = EmployeePersonalInfo.objects.get(emp_id=emp_id)
            EmployeeVerification_model = EmployeeVerification.objects.get(employee=employee_personal_info)
        except:
            EmployeeVerification_model=None
        try:
            employee_personal_info = EmployeePersonalInfo.objects.get(emp_id=emp_id)
            EmployeeSalaryDeduction_model = EmployeeSalaryDeduction.objects.get(employee=employee_personal_info)
        except:
            EmployeeSalaryDeduction_model=None
        try:
            employee_personal_info = EmployeePersonalInfo.objects.get(emp_id=emp_id)
            EmployeeSalaryEarning_model = EmployeeSalaryEarning.objects.get(employee=employee_personal_info)
        except:
            EmployeeSalaryEarning_model=None
        try:
            employee_personal_info = EmployeePersonalInfo.objects.get(emp_id=emp_id)
            EmployeeStatus_model = EmployeeStatus.objects.get(employee=employee_personal_info)
        except:
            EmployeeStatus_model=None
        try:
            employee_personal_info = EmployeePersonalInfo.objects.get(emp_id=emp_id)
            EmployeeLogin_model = EmployeeLogin.objects.get(employee=employee_personal_info)
        except:
            EmployeeLogin_model=None

            




    context={
        'employee_list':employee_list,
        "EmpPersonalInfo":EmpPersonalInfo,
        "EmployeeJobInfo_model":EmployeeJobInfo_model,
        "EmployeeContactInfo_model":EmployeeContactInfo_model,
        "EmployeeFinancialInfo_model":EmployeeFinancialInfo_model,
        "EmployeeDocuments_model":EmployeeDocuments_model,
        "EmployeeHealthInfo_model":EmployeeHealthInfo_model,
        "EmployeeVerification_model":EmployeeVerification_model,
        "EmployeeSalaryDeduction_model":EmployeeSalaryDeduction_model,
        "EmployeeSalaryEarning_model":EmployeeSalaryEarning_model,
        "EmployeeLogin_model":EmployeeLogin_model,
        "EmployeeStatus_model":EmployeeStatus_model,
        "Office_Model":Office_Model,
        "Department_Model":Department_Model,
        "Role_Model":Role_Model,
    }

    return render(request,"CRUD_Employee.html", context)

def Check_Availability(request):
    emp_id = request.GET.get('emp_id', None)
    data = {
        'assigned': EmployeePersonalInfo.objects.filter(emp_id=emp_id).exists(),
        'emp_name': None
    }
    if data['assigned']:
        employee = EmployeePersonalInfo.objects.get(emp_id=emp_id)
        data['emp_name'] = employee.emp_name
    
    return JsonResponse(data)




def Save_Personal_Info(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    if request.method == 'POST':
        try:
            emp_id = request.POST.get('emp_id')
            emp_name = request.POST.get('emp_name')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            photo = request.FILES.get('photo')
            try:
                employee = EmployeePersonalInfo.objects.get(emp_id=emp_id)
            except EmployeePersonalInfo.DoesNotExist:
                employee = EmployeePersonalInfo(emp_id=emp_id)
            employee.emp_name = emp_name
            employee.gender = gender
            employee.dob = dob
            if photo:
                employee.photo = photo
            employee.save()
            request.session['emp_id'] = emp_id
            messages.success(request, 'Employee Personal Info saved successfully!')
        except Exception as e:
            print(e)  # For debugging purposes, this can be removed in production
            messages.error(request, f"An error occurred: {e}")
    return redirect("/Attendance/CRUD_Employee/")
def Save_Job_Info(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    if request.method == 'POST':
        print("##################")

        try:
            # Retrieve the employee ID from the session
            emp_id = request.session.get('emp_id')
            if not emp_id:
                messages.error(request, "Employee ID not found in session.")
                return redirect("/Attendance/CRUD_Employee/")

            print(f"Employee ID from session: {emp_id}")
            employee_personal_info = EmployeePersonalInfo.objects.get(emp_id=emp_id)
            job_info, created = EmployeeJobInfo.objects.get_or_create(employee=employee_personal_info)
            doj = request.POST.get('doj')
            # Ensure this prints a valid date
            designation = request.POST.get('designation')
            office = request.POST.get('office')
            department = request.POST.get('department')
            role = request.POST.get('role')
            qualifications = request.POST.get('qualifications')
            skills = request.POST.get('skills')
            certifications = request.POST.get('certifications')
            achievements = request.POST.get('achievements')

            # Check if the 'doj' is provided
            if not doj:
                messages.error(request, "Date of Joining is required.")
                return redirect("/Attendance/CRUD_Employee/")

            # Update the fields with the submitted data
            job_info.doj = doj
            job_info.designation = designation
            job_info.office = office
            job_info.department = department
            job_info.role = role
            job_info.qualifications = qualifications
            job_info.skills = skills
            job_info.certifications = certifications
            job_info.achievements = achievements

            # Save the updated or newly created job info
            job_info.save()

            messages.success(request, 'Employee Job Info saved successfully!')
        except EmployeePersonalInfo.DoesNotExist:
            messages.error(request, "EmployeePersonalInfo not found.")
        except Exception as e:
            print(f"Error occurred: {e}")
            messages.error(request, f"An error occurred: {e}")
    return redirect("/Attendance/CRUD_Employee/")


def Save_Contact_Info(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    if request.method == 'POST':
        # Fetch the associated employee record
        employee = get_object_or_404(EmployeePersonalInfo, emp_id=request.session['emp_id'])

        try:
            # Fetch or create the EmployeeContactInfo record for the employee
            contact_info, created = EmployeeContactInfo.objects.get_or_create(employee=employee)

            # Update the contact information with the submitted data
            contact_info.mobile = request.POST.get('mobile')
            contact_info.whatsapp = request.POST.get('whatsapp')
            contact_info.email = request.POST.get('email')
            contact_info.residential_address = request.POST.get('residential_address')
            contact_info.work_location = request.POST.get('work_location')
            contact_info.emergency_contact_name = request.POST.get('emergency_contact_name')
            contact_info.emergency_contact_phone = request.POST.get('emergency_contact_phone')
            contact_info.family_contact_details = request.POST.get('family_contact_details')

            # Save the updated contact information
            contact_info.save()

            # Display a success message
            messages.success(request, 'Employee contact information saved successfully!')

        except Exception as e:
            # Display an error message if something goes wrong
            messages.error(request, f"An error occurred: {e}")

    # Redirect back to the employee CRUD page
    return redirect("/Attendance/CRUD_Employee/")
def Save_Financial_Info(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    if request.method == 'POST':
        # Fetch the associated employee record
        employee = get_object_or_404(EmployeePersonalInfo, emp_id=request.session.get('emp_id'))

        try:
            # Fetch or create the EmployeeFinancialInfo record for the employee
            financial_info, created = EmployeeFinancialInfo.objects.get_or_create(employee=employee)

            # Update the financial information with the submitted data
            financial_info.bank_account_number = request.POST.get('bank_account_number')
            financial_info.pan_number = request.POST.get('pan_number')
            financial_info.aadhaar_number = request.POST.get('aadhaar_number')
            financial_info.aadhaar_linked_pan = 'aadhaar_linked_pan' in request.POST

            # Save the updated financial information
            financial_info.save()

            # Display a success message
            messages.success(request, 'Employee financial information saved successfully!')

        except Exception as e:
            # Display an error message if something goes wrong
            messages.error(request, f"An error occurred: {e}")

    # Redirect back to the employee CRUD page
    return redirect("/Attendance/CRUD_Employee/")
def Save_Documents_Info(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    if request.method == 'POST':
        # Fetch the associated employee record
        employee = get_object_or_404(EmployeePersonalInfo, emp_id=request.session.get('emp_id'))

        try:
            # Fetch or create the EmployeeDocuments record for the employee
            documents_info, created = EmployeeDocuments.objects.get_or_create(employee=employee)
            documents_info.previous_employer_details = request.POST.get('previous_employer_details')
            documents_info.previous_employer_contact_mobile = request.POST.get('previous_employer_contact_mobile')
            documents_info.previous_employer_contact_email = request.POST.get('previous_employer_contact_email')
            if 'cibil_report' in request.FILES:
                documents_info.cibil_report = request.FILES['cibil_report']
            if 'pcc' in request.FILES:
                documents_info.pcc = request.FILES['pcc']
            documents_info.save()
            messages.success(request, 'Employee documents information saved successfully!')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return redirect("/Attendance/CRUD_Employee/")
def Save_Health_Info(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    if request.method == 'POST':
        # Fetch the associated employee record using the emp_id stored in the session
        employee = get_object_or_404(EmployeePersonalInfo, emp_id=request.session.get('emp_id'))

        try:
            # Fetch or create the EmployeeHealthInfo record for the employee
            health_info, created = EmployeeHealthInfo.objects.get_or_create(employee=employee)

            # Update the health information with the submitted data
            health_info.blood_group = request.POST.get('blood_group')
            health_info.mental_health = request.POST.get('mental_health')
            health_info.medical_health = request.POST.get('medical_health')

            # Save the updated health information
            health_info.save()

            # Display a success message
            messages.success(request, 'Employee health information saved successfully!')

        except Exception as e:
            # Display an error message if something goes wrong
            messages.error(request, f"An error occurred: {e}")

    # Redirect back to the employee CRUD page
    return redirect("/Attendance/CRUD_Employee/")
def Save_Verification_Info(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    if request.method == 'POST':
        # Fetch the associated employee record using the emp_id stored in the session
        employee = get_object_or_404(EmployeePersonalInfo, emp_id=request.session.get('emp_id'))

        try:
            # Fetch or create the EmployeeVerification record for the employee
            verification_info, created = EmployeeVerification.objects.get_or_create(employee=employee)

            # Update the verification information with the submitted data
            verification_info.residential_address_verification = request.POST.get('residential_address_verification') == 'on'
            verification_info.previous_employer_verification = request.POST.get('previous_employer_verification') == 'on'
            verification_info.residential_address_gps = request.POST.get('residential_address_gps')

            # Save the updated verification information
            verification_info.save()

            # Display a success message
            messages.success(request, 'Employee verification information saved successfully!')

        except Exception as e:
            # Display an error message if something goes wrong
            messages.error(request, f"An error occurred: {e}")

    # Redirect back to the employee CRUD page
    return redirect("/Attendance/CRUD_Employee/")
def Save_Salary_Deduction_Info(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    if request.method == 'POST':
        # Fetch the employee using the emp_id stored in the session
        employee = get_object_or_404(EmployeePersonalInfo, emp_id=request.session.get('emp_id'))

        try:
            # Fetch or create the EmployeeSalaryDeduction record for the employee
            salary_deduction, created = EmployeeSalaryDeduction.objects.get_or_create(employee=employee)

            # Update the deduction information with the submitted data
            salary_deduction.pf = 'pf' in request.POST
            salary_deduction.esic = 'esic' in request.POST
            salary_deduction.pt = 'pt' in request.POST
            salary_deduction.lwf = 'lwf' in request.POST
            salary_deduction.tds = 'tds' in request.POST
            salary_deduction.BSCD = request.POST.get('bscd')
            salary_deduction.employee_lwf_AMT = request.POST.get('employee_lwf_AMT')
            salary_deduction.employers_lwf_AMT = request.POST.get('employers_lwf_AMT')

            # Save the updated deduction information
            salary_deduction.save()

            # Display a success message
            messages.success(request, 'Employee salary deduction information saved successfully!')

        except Exception as e:
            # Display an error message if something goes wrong
            messages.error(request, f"An error occurred: {e}")

    # Redirect back to the employee CRUD page
    return redirect("/Attendance/CRUD_Employee/")




def Save_Salary_Earning_Info(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    if request.method == 'POST':
        print("ok")
        employee = get_object_or_404(EmployeePersonalInfo, emp_id=request.session.get('emp_id'))

        try:
            # Fetch or create the EmployeeSalaryEarning record
            salary_earning, created = EmployeeSalaryEarning.objects.get_or_create(employee=employee)
            print(request.POST.get('basic_salary'))
            # Retrieve form data
            basic_salary = request.POST.get('basic_salary')
            da = request.POST.get('da')
            bonus = 'bonus' in request.POST
            hra = 'hra' in request.POST
            travel_claim_allowed = 'travel_claim_allowed' in request.POST
            overtime_allowance = request.POST.get('overtime_allowance')

            # Validate salary is provided
            if not basic_salary:
                raise ValueError("Salary is required.")

            # Update the EmployeeSalaryEarning record
            salary_earning.basic_salary = basic_salary
            salary_earning.da = da
            salary_earning.Bonus = bonus
            salary_earning.HRA = hra
            salary_earning.travel_claim_allowed = travel_claim_allowed
            salary_earning.overtime_allowance = overtime_allowance or None  # Handle empty overtime_allowance

            # Save the record
            salary_earning.save()
            messages.success(request, 'Employee salary earning information saved successfully!')

        except Exception as e:
            print(e)
            messages.error(request, f"An error occurred: {e}")

    return redirect("/Attendance/CRUD_Employee/")
def Save_Employee_Status(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    if request.method == 'POST':
        try:
            emp_id=request.session.get('emp_id')
            employment_status = request.POST.get('employment_status')
            username = request.POST.get('username')
            password = request.POST.get('password')
            notice_period = 'notice_period' in request.POST
            resigned = 'resigned' in request.POST
            terminated = 'terminated' in request.POST
            dead = 'dead' in request.POST
            training_period = 'training_period' in request.POST
            
            try:
                employee = EmployeePersonalInfo.objects.get(emp_id=emp_id)
                status, created = EmployeeStatus.objects.get_or_create(employee=employee)
                status.employment_status = employment_status
                status.notice_period = notice_period
                status.resigned = resigned
                status.terminated = terminated
                status.dead = dead
                status.training_period = training_period
                status.save()
                messages.success(request, 'Employee status information saved successfully!')
            except EmployeePersonalInfo.DoesNotExist:
                messages.error(request, f"Employee with ID {emp_id} does not exist.")


            try:                
                employee = EmployeePersonalInfo.objects.get(emp_id=emp_id)
                login, created = EmployeeLogin.objects.get_or_create(employee=employee)
                login.username=username
                login.password=password
                login.save()
            except:
                messages.error(request,"Unable To Create User")

                
        except Exception as e:
            print(e)  # For debugging purposes, this can be removed in production
            messages.error(request, f"An error occurred: {e}")
    return redirect("/Attendance/CRUD_Employee/")
def ClearSession(request):    
    if 'emp_id' in request.session:
        del request.session['emp_id']
    messages.success(request,"Employee Session Refresh Successfully")

    return redirect("/Attendance/CRUD_Employee/")
def captch(request):
    # messages.success(request,"ok")
    messages.success(request,"ok")
    return render(request,"captch.html")

def MarkAttendence(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')

    if request.method == 'POST':
        latitude = request.POST.get('Latitude')
        longitude = request.POST.get('Longitude')

        My_Id = request.session['My_Id']  # Assuming employee ID is stored in session
        current_date = timezone.localtime(timezone.now()).date()
        try:
            employee_personal_info = EmployeePersonalInfo.objects.get(emp_id=My_Id)
            try:
                attendance = EmployeeAttendance.objects.get(employee=employee_personal_info, date=current_date)
            except EmployeeAttendance.DoesNotExist:
                attendance = EmployeeAttendance(employee=employee_personal_info, date=current_date)
            if attendance.check_in and not attendance.check_out:
                attendance.check_out = timezone.localtime(timezone.now()).time()
                attendance.check_out_location=f"{latitude}, {longitude}"
                attendance.save()
                messages.success(request, f"Checked out successfully for {current_date}.")
            elif attendance.check_in and attendance.check_out:
                messages.error(request, "Already checked out. Please contact your manager.")
            else:
                attendance.check_in = timezone.localtime(timezone.now()).time()
                attendance.check_in_location=f"{latitude}, {longitude}"
                attendance.save()
                messages.success(request, f"Checked in successfully for {current_date}.")
        except EmployeePersonalInfo.DoesNotExist:
            messages.error(request, "Employee information not found.")
        except Exception as e:
            messages.error(request, f"Oops! Something went wrong due to: {e}")
    return redirect("/Attendance/")



def Report(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')
    
        # Get the start and end date from the request (GET parameters)
    start_date_str = request.GET.get('from_date')
    end_date_str = request.GET.get('end_date')

    # Parse the start and end dates or get default date range
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            start_date, end_date = get_date_range()  # Default date range handling
    else:
        start_date, end_date = get_date_range()



    
    total_days_range = (end_date - start_date).days + 1

    Weekly_Off_days = 0
    sundays = []
    Total_Holidays = 0

    # Loop through each day in the date range to count Sundays and holidays
    for day_offset in range(total_days_range):
        current_date = start_date + timedelta(days=day_offset)
        if current_date.weekday() == 6:  # Sunday
            sundays.append(current_date)
            Weekly_Off_days += 1

    # Query holidays for the custom date range
    holidays = Holiday.objects.filter(
        date__range=(start_date, end_date)
    )
    filtered_holidays = holidays.exclude(date__in=sundays)
    Total_Holidays = filtered_holidays.count()

    # List to store data for all employees
    data = []

    # Iterate over each employee
    EmployeeDetails = EmployeePersonalInfo.objects.all()
    for emp in EmployeeDetails:
        employee_data = userInfo(emp.emp_id)

        # Call the helper function to get attendance and salary details
        calculation_data = calculate_attendance_and_salary(
            emp,
            start_date,  # Use start_date for the year context
            end_date,  # Use start_date for the month context (if needed)
            total_days_range,
            Weekly_Off_days,
            Total_Holidays,
            sundays
        )
        Basic_Salary, Dearness_Allowence, In_Hand = get_Salary_Calculations(emp,calculation_data["Payable_Days"],total_days_range)

        # Append the data to the list
        data.append({
            # Common data
            "Payable_Days": calculation_data["Payable_Days"],
            "Working_Days": calculation_data["Working_Days"],
            "Present_days_count": calculation_data["Present_days_count"],
            "current_month": start_date,
            "current_year": end_date,
            "Total_days": total_days_range,
            "Weekly_Off_days": Weekly_Off_days,
            "sundays": sundays,
            "Total_Holidays": Total_Holidays,
            
            # Personal
            "employee_details": employee_data,
            "Full_days": calculation_data["Full_days"],
            "Half_days": calculation_data["Half_days"],
            "Late_Mark_days": calculation_data["Late_Mark_days"],
            "leave": calculation_data["leave"],
            
            # Salar
            "Basic_Salary": Basic_Salary,
            "Dearness_Allowence": Dearness_Allowence,
            "In_Hand": In_Hand,
        })
    context = {
        'data': data
    }
    return render(request, "Report.html", context)


def IndividualReports(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    if request.method == 'POST':
        latitude = request.POST.get('Latitude')
        longitude = request.POST.get('Longitude')

        My_Id = request.session['My_Id']  # Assuming employee ID is stored in session
    return render(request,"IndividualReports.html")





def Holidays(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    if request.method == 'POST':
        latitude = request.POST.get('Latitude')
        longitude = request.POST.get('Longitude')

        My_Id = request.session['My_Id']  # Assuming employee ID is stored in session
    return render(request,"Holidays.html")





























































import random
from datetime import date, datetime, timedelta
from faker import Faker
from django.shortcuts import redirect
from django.utils import timezone
from .models import EmployeePersonalInfo, EmployeeAttendance, Holiday

fake = Faker()

def add_dummy_attendance(request):
    My_Id = request.session.get('My_Id')  # Assuming employee ID is stored in session
    if not My_Id:
        messages.error(request, "Session expired or invalid employee ID.")
        return redirect("/Attendance/")

    try:
        employee_personal_info = EmployeePersonalInfo.objects.get(emp_id=My_Id)

        # Generate dummy data
        today = timezone.localtime(timezone.now()).date()
        for i in range(1, 60):  # Adding attendance for 10 days
            date = today - timedelta(days=i)
            check_in_time = fake.date_time_this_year(before_now=True, after_now=False).replace(second=0, microsecond=0)
            check_out_time = check_in_time + timedelta(hours=random.randint(6, 9))  # Random work hours between 6 to 9

            # Create and save the attendance record
            attendance = EmployeeAttendance(
                employee=employee_personal_info,
                date=date,
                check_in=check_in_time.time(),
                check_out=check_out_time.time(),
            )
            attendance.save()
        messages.success(request, "Dummy attendance data added successfully.")
    except EmployeePersonalInfo.DoesNotExist:
        messages.error(request, "Employee information not found.")
    except Exception as e:
        messages.error(request, f"Oops! Something went wrong due to: {e}")

    return redirect("/Attendance/")

