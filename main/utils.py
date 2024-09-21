from datetime import timedelta
from decimal import Decimal
from django.contrib import messages
from urllib import request

import requests
from Attendance.models import (
    EmployeeAttendance, EmployeePersonalInfo, EmployeeJobInfo, EmployeeContactInfo, 
    EmployeeFinancialInfo, EmployeeDocuments, EmployeeHealthInfo, 
    EmployeeVerification, EmployeeSalaryDeduction, EmployeeSalaryEarning, 
    EmployeeStatus, EmployeeLogin, EmployeeAccess, Holiday
)
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from main.models import Department, Office, Role

def Validate_Role(emp_id):
    try:
        personal_info = EmployeePersonalInfo.objects.get(emp_id=emp_id)
        job_info = EmployeeJobInfo.objects.get(employee=personal_info)

        role_info = Role.objects.get(pk=job_info.role)
        department_info = Department.objects.get(pk=job_info.department)
        office_info = Office.objects.get(pk=job_info.office)

        return {
            'Role_info': role_info.role_name,
            'Department': department_info.department_name,
            'office': office_info.office_name
        }
    except (EmployeePersonalInfo.DoesNotExist, EmployeeJobInfo.DoesNotExist, Role.DoesNotExist, 
            Department.DoesNotExist, Office.DoesNotExist):
        return None











def userInfo(emp_id):
    try:
        # Fetch the personal information of the employee
        personal_info = EmployeePersonalInfo.objects.get(emp_id=emp_id)
    except EmployeePersonalInfo.DoesNotExist:
        # Return None if personal info does not exist
        return None

    # Initialize other fields to None and handle each case separately
    try:
        job_info = EmployeeJobInfo.objects.get(employee=personal_info)
    except EmployeeJobInfo.DoesNotExist:
        job_info = None

    
    try:
        office_info=Office.objects.get(pk=job_info.office)
    except:
        office_info=None
    try:
        Department_info=Department.objects.get(pk=job_info.department)
    except:
        Department_info=None
    try:
        Role_info=Role.objects.get(pk=job_info.role)
    except:
        Role_info=None


    
    try:
        contact_info = EmployeeContactInfo.objects.get(employee=personal_info)
    except EmployeeContactInfo.DoesNotExist:
        contact_info = None

    try:
        financial_info = EmployeeFinancialInfo.objects.get(employee=personal_info)
    except EmployeeFinancialInfo.DoesNotExist:
        financial_info = None

    try:
        documents = EmployeeDocuments.objects.get(employee=personal_info)
    except EmployeeDocuments.DoesNotExist:
        documents = None

    try:
        health_info = EmployeeHealthInfo.objects.get(employee=personal_info)
    except EmployeeHealthInfo.DoesNotExist:
        health_info = None

    try:
        verification = EmployeeVerification.objects.get(employee=personal_info)
    except EmployeeVerification.DoesNotExist:
        verification = None

    try:
        salary_deduction = EmployeeSalaryDeduction.objects.get(employee=personal_info)
    except EmployeeSalaryDeduction.DoesNotExist:
        salary_deduction = None

    try:
        salary_earning = EmployeeSalaryEarning.objects.get(employee=personal_info)
    except EmployeeSalaryEarning.DoesNotExist:
        salary_earning = None

    try:
        status = EmployeeStatus.objects.get(employee=personal_info)
    except EmployeeStatus.DoesNotExist:
        status = None

    try:
        access = EmployeeAccess.objects.get(employee=personal_info)
    except EmployeeAccess.DoesNotExist:
        access = None

    # Return the information in a dictionary format
    return {
        'personal_info': personal_info,
        'job_info': job_info,
        "office_info":office_info,
        "Department_info":Department_info,
        "Role_info":Role_info,
        'contact_info': contact_info,
        'financial_info': financial_info,
        'documents': documents,
        'health_info': health_info,
        'verification': verification,
        'salary_deduction': salary_deduction,
        'salary_earning': salary_earning,
        'status': status,
        'access': access,
    }










def calculate_attendance_and_salary(emp, start_date, end_date, Total_days, Weekly_Off_days, Total_Holidays, sundays):
    Full_days = 0
    Half_days = 0
    Late_Mark_days = 0
    leave = 0
    Payable_Days = 0
    Present_days_count = 0

    current_date = start_date
    while current_date <= end_date:
        generate_date=current_date

        try:
            holidays_model = Holiday.objects.get(date=generate_date)
        except Holiday.DoesNotExist:
            holidays_model = None

        if holidays_model:
            if holidays_model.type == "FD":
                Full_days += 1
                # Move to the next day
                current_date += timedelta(days=1)

                continue
            else:
                try:
                    find_Attendence = EmployeeAttendance.objects.get(date=generate_date, employee=emp)
                    if find_Attendence.status in ["P", "L"]:
                        Full_days += 1
                        if find_Attendence.status == "L":
                            Late_Mark_days += 1
                    elif find_Attendence.status == "H":
                        Full_days += 1
                    elif find_Attendence.status == "A":
                        leave += 1
                    else:
                        leave += 1
                except EmployeeAttendance.DoesNotExist:
                    leave += 1
        else:
            try:
                find_Attendence = EmployeeAttendance.objects.get(date=generate_date, employee=emp)
                if find_Attendence.status in ["P", "L"]:
                    Full_days += 1
                    if find_Attendence.remark == "Late":
                        Late_Mark_days += 1
                elif find_Attendence.status == "H":
                    Half_days += 1
                elif find_Attendence.status == "A":
                    leave += 1
                else:
                    leave += 1
            except EmployeeAttendance.DoesNotExist:
                leave += 1
        # Move to the next day
        current_date += timedelta(days=1)

    # Calculate Working Days and Payable Days
    Total_Holidays_Including_Weekly_Offs = Weekly_Off_days + Total_Holidays
    Working_Days = Total_days - Total_Holidays_Including_Weekly_Offs
    Present_days_count = Full_days + (Half_days / 2)
    # <====================paid leave calculations============>
    if leave > 0:
        Payable_Days = Present_days_count + 1
    else:
        Payable_Days = Present_days_count
    # <====================End paid leave calculations============>

    # <====================Min Presenty Validation calculations============>
    # if present days will be less than 15 then i will minus the holidays from its payble days because holidays already added in payble days 
    if Payable_Days > 15:
        Payable_Days += Weekly_Off_days
    else:
        Payable_Days -= Total_Holidays
    # <====================End Min Presenty Validation calculations============>

    return {
        "Full_days": Full_days,
        "Half_days": Half_days,
        "Late_Mark_days": Late_Mark_days,
        "leave": leave,
        "Payable_Days": Payable_Days,
        "Present_days_count": Present_days_count,
        "Working_Days": Working_Days,
    }


































































from decimal import Decimal, ROUND_HALF_UP

def get_Salary_Calculations_old(emp, Payable_Days, Total_days):
    try:
        try:
            Earning = EmployeeSalaryEarning.objects.get(employee=emp)
        except:
            Earning=None
        try:
            Deduction = EmployeeSalaryDeduction.objects.get(employee=emp)
        except:
            Deduction=None

        # <================= For TDS ====================>
        if Deduction.tds:
            Present_Days=Payable_Days
            Basic_Salary=Earning.basic_salary
            Per_day=Basic_Salary/Total_days
            Amount=Per_day*Payable_Days
            if Deduction.tds:
                TDS=Basic_Salary*(0.05)
            In_Hand=Amount-TDS
            Basic_Salary = Basic_Salary
            Dearness_Allowence = 0
            In_Hand = In_Hand

        # <================= For PF ====================>
        elif Deduction.pf:
            Present_Days=Payable_Days
            Basic_Salary=Earning.basic_salary
            Dearness_Allowence=Earning.da

            DA_Plus_Basic=Basic_Salary+Dearness_Allowence
            Per_day=DA_Plus_Basic/Present_Days
            # Main Amount
            # bellow deduction and Addition Apllied on This Amount
            Amount=Per_day*Present_Days

            # Addition
            Bonus=HRA=Total_PF=Total_LWF=Total_ESIC=PT=0
            if Earning.Bonus:
                Bonus = Basic_Salary * 0.0833
            if Earning.HRA:
                HRA = Basic_Salary * 0.05
            # Deduction
            if Deduction.pf:
                employee_PF = Basic_Salary * 0.12
                employers_PF = Basic_Salary * 0.13
                Total_PF=employee_PF+employers_PF
            if Deduction.esic:
                if HRA:
                    Basic_plus_da_plus_hra=Basic_Salary+Dearness_Allowence+HRA
                else:
                    Basic_plus_da_plus_hra=Basic_Salary+Dearness_Allowence
                employee_esic=Basic_plus_da_plus_hra * 0.0075
                employers_esic=Basic_plus_da_plus_hra * 0.0325
                Total_ESIC=employee_esic+employers_esic
            if Deduction.pt:
                # Calculations Remains For the february
                if emp.gender=="M":
                    if Basic_Salary<8000:
                        PT=175
                    else:
                        PT=200
            if Deduction.lwf:
                employee_lwf=Deduction.employee_lwf_AMT
                employers_lwf=Deduction.employers_lwf_AMT
                Total_LWF=employee_lwf+employers_lwf
            

            Total_Addition=Bonus+HRA
            Total_Deducion=Total_PF+Total_LWF+Total_ESIC+PT
            In_Hand=Amount+Total_Addition
            In_Hand-=Total_Deducion
            # value passing is remained

            # <================= Return The Values ====================>

            Basic_Salary = Basic_Salary
            Dearness_Allowence = Dearness_Allowence
            In_Hand = In_Hand


        else:
            Basic_Salary = "-"
            Dearness_Allowence = "-"
            In_Hand = "Error"
        if Total_days<28:
            Basic_Salary = "-"
            Dearness_Allowence = "-"
            In_Hand = "Please select a valid date range"
    except Exception as e:
        print(e)
        Basic_Salary=Dearness_Allowence=In_Hand=e
        # Basic_Salary=Dearness_Allowence=In_Hand="Oops"
        pass
    
    return Basic_Salary, Dearness_Allowence, In_Hand
from decimal import Decimal, getcontext

# Set the precision for Decimal operations
getcontext().prec = 10

def get_Salary_Calculations(emp, Payable_Days, Total_days):
    try:
        # Fetching Earning and Deduction objects
        Earning = EmployeeSalaryEarning.objects.filter(employee=emp).first()
        Deduction = EmployeeSalaryDeduction.objects.filter(employee=emp).first()

        # Initialize variables
        Basic_Salary = Decimal(0)
        Dearness_Allowence = Decimal(0)
        In_Hand = Decimal(0)

        # Check if Total_days is valid to avoid division by zero
        if Total_days <= 0:
            raise ValueError("Total_days must be greater than 0")
        if Payable_Days > 0:
            raise ValueError("Payble Days must be greater than 0")

        # <================= For TDS ====================>
        if Deduction and Deduction.tds:
            if Earning and Earning.basic_salary is not None:
                Basic_Salary = Decimal(Earning.basic_salary)
                Per_day = Basic_Salary / Decimal(Total_days)
                Amount = Per_day * Decimal(Payable_Days)
                TDS = Basic_Salary * Decimal(0.05)
                In_Hand = Amount - TDS
                Dearness_Allowence = Decimal(0)

        # <================= For PF ====================>
        elif Deduction and Deduction.pf:
            if Earning and Earning.basic_salary is not None:
                Basic_Salary = Decimal(Earning.basic_salary)
                Dearness_Allowence = Decimal(Earning.da)

                DA_Plus_Basic = Basic_Salary + Dearness_Allowence
                Per_day = DA_Plus_Basic / Decimal(Deduction.BSCD)
                Amount = Per_day * Decimal(Payable_Days)

                # Initialize addition and deduction values
                Bonus = HRA = Total_PF = Total_LWF = Total_ESIC = PT = Decimal(0)

                if Earning.Bonus:
                    Bonus = Basic_Salary * Decimal(0.0833)
                if Earning.HRA:
                    HRA = Basic_Salary * Decimal(0.05)

                # Deduction for PF
                if Deduction.pf:
                    employee_PF = Basic_Salary * Decimal(0.12)
                    employers_PF = Basic_Salary * Decimal(0.13)
                    Total_PF = employee_PF + employers_PF

                # Deduction for ESIC
                if Deduction.esic:
                    Basic_plus_da_plus_hra = Basic_Salary + Dearness_Allowence + (HRA if Earning.HRA else Decimal(0))
                    employee_esic = Basic_plus_da_plus_hra * Decimal(0.0075)
                    employers_esic = Basic_plus_da_plus_hra * Decimal(0.0325)
                    Total_ESIC = employee_esic + employers_esic

                # Deduction for PT
                if Deduction.pt:
                    if emp.gender == "M":
                        PT = Decimal(175) if Basic_Salary < Decimal(8000) else Decimal(200)

                # Deduction for LWF
                if Deduction.lwf:
                    employee_lwf = Decimal(Deduction.employee_lwf_AMT)
                    employers_lwf = Decimal(Deduction.employers_lwf_AMT)
                    Total_LWF = employee_lwf + employers_lwf

                # Calculate total addition and deduction
                Total_Addition = Bonus + HRA
                Total_Deduction = Total_PF + Total_LWF + Total_ESIC + PT
                In_Hand = Amount + Total_Addition - Total_Deduction

                # Final values
                Dearness_Allowence = Dearness_Allowence

        else:
            Basic_Salary = "-"
            Dearness_Allowence = "-"
            In_Hand = "Error"

        if Total_days < 28:
            Basic_Salary = "-"
            Dearness_Allowence = "-"
            In_Hand = "Please select a valid date range"

    except Exception as e:
        Basic_Salary ='-'
        Dearness_Allowence = '-'
        In_Hand = e
    
    # Formatting to 3 decimal places if not an error string
    if isinstance(Basic_Salary, Decimal):
        Basic_Salary = Basic_Salary.quantize(Decimal('0.001'))
    if isinstance(Dearness_Allowence, Decimal):
        Dearness_Allowence = Dearness_Allowence.quantize(Decimal('0.001'))
    if isinstance(In_Hand, Decimal):
        In_Hand = In_Hand.quantize(Decimal('0.001'))

    return Basic_Salary, Dearness_Allowence, In_Hand
