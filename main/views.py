from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages  # Import the messages module

from Attendance.models import EmployeeJobInfo, EmployeeLogin
from main.models import Department, Office, Role
from main.utils import Validate_Role

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Authenticate the user
            user = EmployeeLogin.objects.get(username=username, password=password)
            employee = user.employee

            # Store session data
            request.session['My_Id'] = employee.emp_id
            return redirect('/Attendance/')  # Redirect to dashboard or any other page after successful login

        except EmployeeLogin.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('/')  # Redirect back to the login page on failure

    return render(request, "EMPlogin.html")
def logout(request):
    request.session.flush()
    return redirect("/")










def AdvanceOptions(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    try:
        OfficeModel=Office.objects.all()
    except:
        OfficeModel=None
    try:
        DepartmentModel=Department.objects.all()
    except:
        DepartmentModel=None
    try:
        RoleModel=Role.objects.all()
    except:
        RoleModel=None
    context={
        'Office':OfficeModel,
        'Departments':DepartmentModel,
        'Roles':RoleModel,
 
    }
    return render(request,"AdvanceOptions.html",context)

def AddOffice(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    if request.method == "POST":
        office_name = request.POST.get('office_name')
        office_code = request.POST.get('office_code')
        location = request.POST.get('location')
        date_of_establishment = request.POST.get('date_of_establishment')
        ceo = request.POST.get('ceo')
        staff_count = request.POST.get('staff_count')
        remark = request.POST.get('remark')

        # Create and save the new office object
        new_office = Office(
            office_name=office_name,
            office_code=office_code,
            location=location,
            date_of_establishment=date_of_establishment,
            ceo=ceo,
            staff_count=staff_count,
            remark=remark
        )
        try:
            new_office.save()
            messages.success(request,f"Office Added Successfully")

        except Exception as e:
            messages.success(request,f"Unable to Add Office Due To:{e}")
    return redirect("/AdvanceOptions/")


def AddDepartment(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    if request.method == "POST":
        department_name = request.POST.get('department_name')
        # Create and save the new office object
        new_Department = Department(
            department_name=department_name,  
        )
        try:
            new_Department.save()
            messages.success(request,f"Department Added Successfully")

        except Exception as e:
            messages.success(request,f"Unable to Add Department Due To:{e}")
    return redirect("/AdvanceOptions/")


def AddRoles(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')
    role_info = Validate_Role(request.session['My_Id'])
    if not role_info or role_info['Role_info'] != "Hiring Manager":
        return redirect('/logout/')

    if request.method == "POST":
        role_name = request.POST.get('role_name')
        # Create and save the new office object
        new_Role = Role(
            role_name=role_name,
        )
        try:
            new_Role.save()
            messages.success(request,f"Role Added Successfully")

        except Exception as e:
            messages.success(request,f"Unable to Add Role Due To:{e}")
    return redirect("/AdvanceOptions/")