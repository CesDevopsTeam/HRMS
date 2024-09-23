from django.shortcuts import render

from kpi.models import KRA
from main.models import Role
from main.utils import userInfo

# Create your views here.
def dashboard(request):
    employee_data = userInfo(request.session['My_Id'])
    context={
        'employee_data': employee_data,

        }
    return render(request,"KPI_Dashboard.html", context)
def kra(request):
    employee_data = userInfo(request.session['My_Id'])
    KRA_data = []
    Role_Model = Role.objects.all()

    for Role_OBJ in Role_Model:
        try:
            KRA_Model = KRA.objects.filter(role=Role_OBJ).first()  # Use Role_OBJ here and call first() with parentheses
            All_KRA_Model = KRA.objects.filter(role=Role_OBJ)
        except KRA.DoesNotExist:
            KRA_Model = None
            All_KRA_Model = None
            
        KRA_data.append({
            'Role': Role_OBJ,
            'KRA_Model': KRA_Model,
            'All_KRA_Model': All_KRA_Model,
        })

    print(KRA_data)  # This will show the KRA data in the console for debugging

    context = {
        'KRA_data': KRA_data,
        'employee_data': employee_data,
    }
    return render(request, "kra.html", context)
