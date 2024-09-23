from django.shortcuts import render, redirect
from Attendance.models import EmployeePersonalInfo
from django.shortcuts import redirect, get_object_or_404

from main.utils import userInfo
# Example import in views.py or admin.py
from .models import Task
from django.contrib.auth.decorators import login_required
from datetime import date
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import EmployeePersonalInfo, Task
from django.shortcuts import render, redirect
from .models import Task,Rating
from Attendance.models import EmployeePersonalInfo
from django.utils.dateparse import parse_date
from datetime import date
from django.contrib import messages  # Import the messages module

def task(request):
    if 'My_Id' not in request.session:
        return redirect('/logout/')

    employee = None
    tasks_by_date = {}
    searched = False
    username = None

    # Handle GET request
    if request.method == 'GET':
        emp_id = request.GET.get('emp_id', None)
        emp_name = request.GET.get('emp_name', None)  # Get employee name from the search input

        if emp_id:
            searched = True
            try:
                employee = EmployeePersonalInfo.objects.get(emp_id=emp_id)
                username = employee.emp_name
                tasks = Task.objects.filter(employee=employee)
            except EmployeePersonalInfo.DoesNotExist:
                employee = None

        # Search by employee name
        if emp_name:
            searched = True
            try:
                employee = EmployeePersonalInfo.objects.get(emp_name__icontains=emp_name)  # Search by name
                username = employee.emp_name
                tasks = Task.objects.filter(employee=employee)
            except EmployeePersonalInfo.DoesNotExist:
                employee = None

    # If no username, get the employee from session
    if not username:
        try:
            emp_id = request.session['My_Id']
            employee = EmployeePersonalInfo.objects.get(emp_id=emp_id)
            username = employee.emp_name
            tasks = Task.objects.filter(employee=employee)
        except KeyError:
            return redirect('/logout/')
        except EmployeePersonalInfo.DoesNotExist:
            pass

    # Handle POST request
    if request.method == 'POST':
        emp_id = request.POST.get('employee_id')
        task_title = request.POST.get('task_title')
        task_description = request.POST.get('task_description')
        complete_before = request.POST.get('complete_before')
        document = request.FILES.get('document')

        try:
            employee_to_assign = EmployeePersonalInfo.objects.get(emp_id=emp_id)

            # Create the task object including task_title
            Task.objects.create(
                employee=employee_to_assign,
                assigned_by=employee,
                task_title=task_title,
                task_description=task_description,
                complete_before=complete_before,
                document=document
            )

            # Add success message
            messages.success(request, 'Task assigned successfully!')
            return redirect('assigned_tasks')  # Redirect to the assigned tasks page
        except EmployeePersonalInfo.DoesNotExist:
            messages.error(request, 'Employee not found.')

    # Organize tasks by date for display
    if employee:
        tasks = Task.objects.filter(employee=employee)
        for task in tasks:
            task_date = task.assigned_at.date()
            if task_date not in tasks_by_date:
                tasks_by_date[task_date] = []
            tasks_by_date[task_date].append(task)

    # Calculate average rating for completed tasks
    total_score = 0
    count = 0
    completed_tasks = Task.objects.filter(employee=employee, is_completed=True)

    for task in completed_tasks:
        if task.ratings.count() > 0:
            total_score += sum(rating.score for rating in task.ratings.all())
            count += task.ratings.count()

    average_rating = total_score / count if count > 0 else 0

    # Retrieve employee data
    employee_data = userInfo(request.session['My_Id'])

    return render(request, 'task.html', {
        'employee_data': employee_data,  # Pass employee data to the template
        'employee': employee,
        'searched': searched,
        'username': username,
        'tasks_by_date': tasks_by_date,
        'average_rating': average_rating  # Add average rating to context
    })



def daily_task_view(request):
    emp_id = request.session.get('My_Id')
    if not emp_id:
        return redirect('/logout/')
    
    try:
        employee = EmployeePersonalInfo.objects.get(emp_id=emp_id)
        username = employee.emp_name

        # Get date filter from request
        date_filter = request.GET.get('date_filter')
        
        # If no date filter is provided, default to today's date
        if date_filter:
            tasks = Task.objects.filter(employee=employee, assigned_at__date=date_filter).order_by('-assigned_at')
        else:
            today = timezone.now().date()
            tasks = Task.objects.filter(employee=employee, assigned_at__date=today).order_by('-assigned_at')

        # Calculate average rating for completed tasks
        total_score = 0
        count = 0
        completed_tasks = Task.objects.filter(employee=employee, is_completed=True)

        for task in completed_tasks:
            if task.ratings.count() > 0:
                total_score += sum(rating.score for rating in task.ratings.all())
                count += task.ratings.count()

        average_rating = total_score / count if count > 0 else 0
        
        employee_data = userInfo(request.session['My_Id'])
        show_filter=True
        return render(request, 'daily_task.html', {
            'show_filter':show_filter,
            'employee_data':employee_data,
            'tasks': tasks,
            'username': username,
            'date_filter': date_filter,
            'average_rating': average_rating  # Add average rating to context
        })
    except EmployeePersonalInfo.DoesNotExist:
        return redirect('/logout/')

    
   
def mark_task_completed(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.is_completed = True
            task.save()
            messages.success(request, 'Task Completed  successfully!')
            return redirect('daily_task')
        except Task.DoesNotExist:
            return redirect('daily_task')
        
def task_assign_view(request):
    # Retrieve employee data
    emp_id = request.session.get('My_Id')
    employee_data = userInfo(emp_id)  # Assuming you have this function to fetch employee data
    return render(request, 'task_assign.html', {'employee_data': employee_data})


def assign_task_view(request):
    if request.method == 'POST':
        emp_id = request.POST.get('employee_id')
        task_description = request.POST.get('task_description')
        try:
            employee = EmployeePersonalInfo.objects.get(emp_id=emp_id)
            Task.objects.create(employee=employee, task_description=task_description)
            messages.success(request, 'Task assigned successfully!')
            return redirect('task_assign')
        except EmployeePersonalInfo.DoesNotExist:
            messages.error(request, 'Employee does not exist.')
            return redirect('task_assign')

    return render(request, 'assign_task.html')


def completed_tasks_view(request):
    emp_id = request.session.get('My_Id')
    if not emp_id:
        return redirect('/logout/')

    try:
        employee = EmployeePersonalInfo.objects.get(emp_id=emp_id)
        completed_tasks = Task.objects.filter(employee=employee, is_completed=True).order_by('-assigned_at')

        # Fetch associated ratings for each completed task
        for task in completed_tasks:
            task.ratings_list = task.ratings.all()

        return render(request, 'completed_tasks.html', {'tasks': completed_tasks, 'username': employee.emp_name})
    except EmployeePersonalInfo.DoesNotExist:
        return redirect('/logout/')
 

def acknowledge_task_view(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        if not task.is_acknowledged:
            task.is_acknowledged = True
            task.save()
            messages.success(request, 'Task acknowledged successfully!')
    return redirect('daily_task')

def navbar(request):
    return render(request, 'navbar.html')


def overdue_tasks_view(request):
    emp_id = request.session.get('My_Id')
    if not emp_id:
        return redirect('/logout/')
    
    try:
        # Fetch the logged-in employee
        employee = EmployeePersonalInfo.objects.get(emp_id=emp_id)
        username = employee.emp_name
        today = timezone.now().date()
        
        # Filter overdue tasks specific to the logged-in employee
        overdue_tasks = Task.objects.filter(employee=employee, complete_before__lt=today, is_completed=False)

        # Calculate average rating for completed tasks
        total_score = 0
        count = 0
        completed_tasks = Task.objects.filter(employee=employee, is_completed=True)

        for task in completed_tasks:
            if task.ratings.count() > 0:
                total_score += sum(rating.score for rating in task.ratings.all())
                count += task.ratings.count()

        average_rating = total_score / count if count > 0 else 0
        
        # Retrieve employee data
        employee_data = userInfo(emp_id)
        
        return render(request, 'overdue_tasks.html', {
            'employee_data': employee_data,
            'overdue_tasks': overdue_tasks,
            'username': username,
            'average_rating': average_rating
        })
    except EmployeePersonalInfo.DoesNotExist:
        return redirect('/logout/')


def assigned_tasks_view(request):
    emp_id = request.session.get('My_Id')

    if not emp_id:
        return redirect('/logout/')

    try:
        employee = EmployeePersonalInfo.objects.get(emp_id=emp_id)
    except EmployeePersonalInfo.DoesNotExist:
        return redirect('/logout/')

    # Get the current date for default filter
    current_date = timezone.now().date()

    # Get the selected date and employee name from request
    selected_date = request.GET.get('date', str(current_date))
    employee_name = request.GET.get('employee_name', '')

    # Validate selected_date to avoid empty string
    if not selected_date:
        selected_date = str(current_date)

    # Filter tasks assigned on the selected date and optionally by employee name
    assigned_tasks = Task.objects.filter(assigned_by=employee, assigned_at__date=selected_date)

    if employee_name:
        assigned_tasks = assigned_tasks.filter(employee__emp_name__icontains=employee_name)

    # Add ratings to each task
    for task in assigned_tasks:
        task.ratings_list = task.ratings.all()

    # Calculate average rating for completed tasks
    total_score = 0
    count = 0
    completed_tasks = Task.objects.filter(employee=employee, is_completed=True)

    for task in completed_tasks:
        if task.ratings.count() > 0:
            total_score += sum(rating.score for rating in task.ratings.all())
            count += task.ratings.count()

    average_rating = total_score / count if count > 0 else 0

    # Retrieve employee data
    employee_data = userInfo(emp_id)

    context = {
        'employee_data': employee_data,
        'employee': employee,
        'assigned_tasks': assigned_tasks,
        'current_date': current_date,
        'selected_date': selected_date,
        'employee_name': employee_name,
        'average_rating': average_rating
    }

    return render(request, 'assigned_tasks.html', context)




def submit_rating(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        emp_id = request.session.get('My_Id')

        if not emp_id:
            return redirect('/logout/')

        try:
            employee = EmployeePersonalInfo.objects.get(emp_id=emp_id)
        except EmployeePersonalInfo.DoesNotExist:
            return redirect('/logout/')

        score = request.POST.get('score')
        comment = request.POST.get('comment')

        # Assuming the task has an `employee` field that refers to the employee being rated
        rated_to = task.employee  # Replace this with your logic for determining who is being rated

        # Create or update the rating
        rating, created = Rating.objects.update_or_create(
            task=task,
            employee=employee,
            rated_to=rated_to,  # Set the rated_to field here
            defaults={'score': score, 'comment': comment}
        )

        return redirect('assigned_tasks')  # Redirect back to assigned tasks view

def tasks_with_ratings_view(request):
    emp_id = request.session.get('My_Id')
    if not emp_id:
        return redirect('/logout/')

    try:
        employee = EmployeePersonalInfo.objects.get(emp_id=emp_id)
        completed_tasks = Task.objects.filter(employee=employee, is_completed=True).order_by('-assigned_at')

        total_score = 0
        count = 0

        # Fetch associated ratings for each completed task and calculate the total score
        for task in completed_tasks:
            task.ratings_list = task.ratings.all()  # Fetch the ratings related to this task
            if task.ratings.count() > 0:
                total_score += sum(rating.score for rating in task.ratings.all())
                count += task.ratings.count()

        average_rating = total_score / count if count > 0 else 0

        # Retrieve employee data
        employee_data = userInfo(emp_id)

        return render(request, 'tasks_with_ratings.html', {
            'tasks': completed_tasks,
            'username': employee.emp_name,
            'average_rating': average_rating,
            'employee_data': employee_data  # Pass employee data to the template
        })
    except EmployeePersonalInfo.DoesNotExist:
        return redirect('/logout/')