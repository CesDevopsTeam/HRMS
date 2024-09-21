from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from Attendance.models import EmployeeJobInfo, EmployeePersonalInfo
from main.models import Department, Office, Role
from main.utils import Validate_Role
from notifications.models import LeaveRequest, Notification
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from notifications.utils import store_notification

# Create your views here.
def Notifications(request):
    employee_id = request.session['My_Id']
    employee=EmployeePersonalInfo.objects.get(emp_id=employee_id)
    Notification_Model=Notification.objects.filter(recipient=employee).order_by('-created_at')


    Notification_Success=Notification.objects.filter(notification_type='success',recipient=employee).order_by('-created_at')
    Notification_Info=Notification.objects.filter(notification_type='info',recipient=employee).order_by('-created_at')
    Notification_Warning=Notification.objects.filter(notification_type='warning',recipient=employee).order_by('-created_at')
    Notification_Error=Notification.objects.filter(notification_type='error',recipient=employee).order_by('-created_at')
    users = EmployeePersonalInfo.objects.all()
    context={
        'users':users,
        'Notification_Model':Notification_Model,
        'Notification_Success':Notification_Success,
        'Notification_Info':Notification_Info,
        'Notification_Warning':Notification_Warning,
        'Notification_Error':Notification_Error,
    }
    return render(request,"Notifications.html",context)
def mark_notification_as_read(request, pk):
    # Fetch the notification
    try:
        notification = Notification.objects.get(pk=pk)
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification does not exist'})










def send_notification(request):
    if request.method == 'POST':
        recipients_ids = request.POST.getlist('recipients')
        message = request.POST.get('message')
        notification_type = request.POST.get('notification_type')
        
        sender = request.user.employee_personal_info  # Assuming the user profile is linked to EmployeePersonalInfo

        for recipient_id in recipients_ids:
            recipient = EmployeePersonalInfo.objects.get(id=recipient_id)
            Notification.objects.create(
                sender=sender,
                recipient=recipient,
                message=message,
                notification_type=notification_type
            )
        
        return redirect('/Notifications/')  # Redirect to a success page or another view

def leave(request):
    if 'My_Id' not in request.session:
        return redirect('/')  # Redirect to login page if session is invalid
    employee_id = request.session['My_Id']

    if request.method == 'POST':
        leave_type = request.POST.get('leaveType')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        leave_duration = request.POST.get('leaveDuration')
        subject = request.POST.get('subject')
        reason = request.POST.get('reason')
        employee_id = request.session['My_Id']

        # Handle file upload
        supporting_document = request.FILES.get('supportingDocument')
        if supporting_document:
            fs = FileSystemStorage()
            filename = fs.save(supporting_document.name, supporting_document)
            supporting_document_url = fs.url(filename)
        else:
            supporting_document_url = None

        # Create the LeaveRequest object

        try:
            employee = EmployeePersonalInfo.objects.get(emp_id=employee_id)
        except EmployeePersonalInfo.DoesNotExist:
            employee = None

        try:
            job_info = EmployeeJobInfo.objects.get(employee=employee)
        except EmployeeJobInfo.DoesNotExist:
            job_info = None
        # Save the leave request
        try:
            LeaveRequest.objects.create(
                employee=employee,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                leave_duration=leave_duration,
                subject=subject,
                reason=reason,
                office=job_info.office,
                department=job_info.department,
                role=job_info.role,
                supporting_document=supporting_document_url
            )
            
            # Display success message
            try:
                Role_Model=Role.objects.filter(role_name="Project Manager").first()
                EmployeeJobInfo_Model=EmployeeJobInfo.objects.filter(office=job_info.office,department=job_info.department,role=Role_Model.pk).first()
                recipient=EmployeeJobInfo_Model.employee
                message = f"New Leave Request from {employee.emp_name} (ID: {employee.emp_id}) for {leave_type} from {start_date} to {end_date}."
                try:
                    redirect_URL="/Notifications/leave/"
                    notification_type='info'
                    notify=store_notification(employee,recipient,message, notification_type,redirect_URL)
                except:
                    pass
            except:
                pass
            messages.success(request, 'Leave request submitted successfully!')
        except Exception as e:
            print(e)
            messages.error(request,f"Oops Something Wrong!{e}")
        return redirect('/Notifications/leave/')

    else:
        My_Team_Leaves=None
        My_Leaves=None
        # Create the LeaveRequest object
        try:
            employee = EmployeePersonalInfo.objects.get(emp_id=employee_id)
        except EmployeePersonalInfo.DoesNotExist:
            employee = None
        My_Leaves=LeaveRequest.objects.filter(employee=employee).order_by('-leave_applied_on')

        role_info = Validate_Role(request.session['My_Id'])
        if role_info['Role_info'] == "Project Manager" or role_info['Role_info'] == "Hiring Manager":
            EmployeeJobInfo_model=EmployeeJobInfo.objects.get(employee=employee)
            My_Team_Leaves=LeaveRequest.objects.filter(office=EmployeeJobInfo_model.office,department=EmployeeJobInfo_model.department,).exclude(employee=employee).order_by('-leave_applied_on')









        return render(request, 'leave.html', {
            'ok':"yes",
            'my_leaves': My_Leaves,
            'My_Team_Leaves':My_Team_Leaves,
        })




def leave_approve(request):
    role_info = Validate_Role(request.session['My_Id'])
    if role_info['Role_info'] != "Project Manager":
        redirect("/")

    try:

        if request.method == 'POST':
            leave_id = request.POST.get('pk')
            status = request.POST.get('status')
            remark = request.POST.get('remark', '')

            # Fetch the leave request instance
            try:
                leave_request = get_object_or_404(LeaveRequest, pk=leave_id)
                EmployeePersonalInfo_model=EmployeePersonalInfo.objects.get(emp_id=request.session['My_Id'])

                # Update the approval status based on the selected option
                if status == 'A':
                    leave_request.is_approved = True
                    leave_request.approved_on = timezone.now()
                    leave_request.approved_by = EmployeePersonalInfo_model  # Assuming the approver is the current logged-in user
                    message = f"Your Leave Request has Been Approved By Project Manager."
                    messages.success(request, f"Leave request for {leave_request.employee.emp_name} has been approved.")
                elif status == 'R':
                    leave_request.is_approved = False
                    leave_request.approved_on = timezone.now()
                    leave_request.approved_by = EmployeePersonalInfo_model
                    message = f"Your Leave Request has Been Rejected :{remark}."
                    messages.warning(request, f"Leave request for {leave_request.employee.emp_name} has been rejected.")

                # Save the remark if any
                leave_request.remark = remark

                # Save the updated leave request
                leave_request.save()


                            # Display success message
                try:
                    sender=EmployeePersonalInfo.objects.get(emp_id=request.session['My_Id'])
                    recipient=leave_request.employee
                    try:
                        redirect_URL="/Notifications/leave/"
                        notification_type='info'
                        notify=store_notification(sender,recipient,message,notification_type,redirect_URL)
                    except:
                        pass
                except:
                    pass




                messages.success(request,"Chnages Made Successfully")
            except Exception as e:
                print(e)
                messages.error(request,f"Unable To Make Changes: {e}")
            return redirect('/Notifications/leave/')  # Redirect to the page that lists the leave requests
    except Exception as e:
        messages.error(request,"Oops Something Went Wrong!")

    return redirect('/Notifications/leave/')  # Fallback in case the method is not POST
