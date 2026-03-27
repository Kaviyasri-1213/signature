from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Employee
from .models import Signup
from django.contrib.auth.hashers import make_password, check_password
from django.views.generic import ListView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth import authenticate, login  as auth_login



# Create your views here.
def login_view(request):
       if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = Signup.objects.get(user=username)
            if check_password(password, user.pasw):
                messages.success(request, "Login Successful!")
                request.session['user_id'] = user.id
                return redirect('details')
            else:
                messages.error(request, "Invalid username or password!")
        except Signup.DoesNotExist:
            messages.error(request, "Invalid username or password!")
       return render(request, "login.html")
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')   
        confirm_password = request.POST.get('rpass')
        email = request.POST.get('epass')
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        if Signup.objects.filter(user=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        if Signup.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')
        obj = Signup()
        obj.user = username
        obj.pasw = make_password(password)   
        obj.email = email
        obj.save()

        messages.success(request, "Sign-up successful! Please login.")
        return redirect('login')
    return render(request, 'signup.html')

def details(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        adhar_number = request.POST.get('adhar_number')
        worked_hours = request.POST.get('worked_hours')
        gender = request.POST.get('gender')
        if Employee.objects.filter(adhar_number=adhar_number).exists():
            messages.error(request, f"Adhar number {adhar_number} already exists!")
            return redirect('details')
        if Employee.objects.filter(email=email).exists():
            messages.error(request, f"Email {email} already exists!")
            return redirect('details')
        email = request.POST.get('email')

        try:
           validate_email(email)
        except ValidationError:
           messages.error(request, "Invalid email format!")
           return redirect('details')

        emp = Employee(
            name=name,
            age=age,
            email=email,
            phone=phone,
            address=address,
            adhar_number=adhar_number,
            worked_hours=worked_hours,
            gender=gender
        )
        emp.save()
        messages.success(request, f"Employee {name} added successfully!")
        return redirect('dashboard')
    
    return render(request, 'details.html')
class EmployeeListView(ListView):
    model = Employee
    template_name = 'dashboard.html'
    context_object_name = 'employees'
    paginate_by = 5

    def get_queryset(self):
        search = self.request.GET.get('search')
        queryset = Employee.objects.all().order_by('-id')

        if search:
            queryset = queryset.filter(
                name__icontains=search
            ) | Employee.objects.filter(
                adhar_number__icontains=search
            )

        return queryset
def logout(request):
    messages.success(request, "Logged out successfully!")
    return redirect('login')
def update(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    if request.method == 'POST':
        emp.name = request.POST.get('name')
        emp.age = request.POST.get('age')
        emp.email = request.POST.get('email')
        emp.phone = request.POST.get('phone')
        emp.gender = request.POST.get('gender')
        emp.address = request.POST.get('address')
        emp.adhar_number = request.POST.get('adhar_number')
        emp.worked_hours = request.POST.get('worked_hours')
        emp.save()
        messages.success(request, f"{emp.name} updated successfully!")
        return redirect('dashboard')
    return render(request, 'update.html', {'emp': emp})
def delete(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    emp.delete()
    messages.success(request, f"{emp.name} deleted successfully!")
    return redirect('dashboard')

def search_suggestions(request):
    term = request.GET.get('term', '')
    employees = Employee.objects.filter(name__icontains=term)[:5]

    data = []
    for emp in employees:
        data.append(emp.name)

    return JsonResponse(data, safe=False)