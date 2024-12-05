from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Signin, Complaint, Department, Category
from django.contrib.auth import logout as django_logout, login as django_login  # Renamed login to avoid conflict
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User



# Login View
def login(request):
    if request.method == 'POST':
        username = request.POST.get('logname')
        password = request.POST.get('logpwd')

        try:
            user = Signin.objects.get(Username=username, Password=password)
            request.session['user'] = user.Username  

            if user.is_super_admin:
                return redirect('super_admin_dashboard')  # Redirect to super admin dashboard
            elif user.is_admin:
                if user.department:
                    request.session['department_id'] = user.department.id
                return redirect('admin_dashboard') # Redirect to admin dashboard
            else:
                return redirect('home')  # Redirect to user dashboard
        except Signin.DoesNotExist:
            return render(request, "login.html", {"message": "Username or password does not exist"})

    return render(request, "login.html")



# Signup View
def sign(request):
    if request.method == 'POST':
        name = request.POST.get('regname').strip()
        email = request.POST.get('regemail').strip()
        uname = request.POST.get('reguname').strip()
        pwd = request.POST.get('regpwd').strip()
        cpwd = request.POST.get('regconfpwd').strip()

        if not name or not email or not uname or not pwd or not cpwd:
            return render(request, "sign.html", {"message": "All fields are required."})

        if pwd == cpwd:
            user = Signin(Name=name, Email=email, Username=uname, Password=pwd)
            user.save()
            return redirect('login')
        else:
            return render(request, "sign.html", {"message": "Passwords do not match."})
    return render(request, "sign.html")

# Home View
def home(request):
    if 'user' not in request.session:
        return redirect('login')  # Redirect to login if user not logged in
    username = request.session.get('user')
    return render(request, "home.html", {'username': username})

# Track Complaint View
def track_complaint(request):
    if 'user' not in request.session:
        return redirect('login')
    user = Signin.objects.get(Username=request.session.get("user"))  # Get logged-in user
    complaints = Complaint.objects.filter(user=user).order_by('-created_at')  # Filter complaints by user
    return render(request, 'track_complaint.html', {'complaints': complaints})

# Register Complaint View
@login_required
def register_complaint(request):
    user = get_logged_in_user(request) 
    if not user:
        return redirect('login')  
    
    departments = Department.objects.all()  
    categories = Category.objects.all()  

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        priority = request.POST.get('priority')
        department_id = request.POST.get('department')
        attachment = request.FILES.get('attachment')  

        if title and description and category_id and priority and department_id:
            try:
                category = Category.objects.get(id=category_id)  
                department = Department.objects.get(id=department_id)  

                complaint = Complaint(
                    user=user, 
                    title=title,
                    description=description,
                    category=category,
                    priority=priority,
                    department=department,
                    attachment=attachment,
                )
                complaint.save()  

                return redirect('track_complaint')  # Redirect to track complaints page
            except Category.DoesNotExist or Department.DoesNotExist:
                return render(request, 'register_complaint.html', {
                    'departments': departments,
                    'categories': categories,
                    'message': 'Invalid category or department.'
                })
        else:
            return render(request, 'register_complaint.html', {
                'departments': departments,
                'categories': categories,
                'message': 'All fields are required.'
            })

    return render(request, 'register_complaint.html', {
        'departments': departments,
        'categories': categories,
    })


def edit_complaint(request, complaint_id):
    
    user = get_logged_in_user(request)
    if not user:
        return redirect('login') 

    try:
       
        complaint = Complaint.objects.get(id=complaint_id, user=user)
    except Complaint.DoesNotExist:
       
        return redirect('track_complaint')

    
    if complaint.status.lower() == "verified":
        messages.warning(request, "Verified complaints cannot be edited or deleted.")
        return redirect('track_complaint')

    if request.method == 'POST':
        # Retrieve form data
        title = request.POST.get('title', complaint.title).strip()
        description = request.POST.get('description', complaint.description).strip()
        attachment = request.FILES.get('attachment')

        complaint.title = title
        complaint.description = description
        if attachment:  
            complaint.attachment = attachment

        
        complaint.save()

        
        messages.success(request, "Complaint updated successfully!")
        return redirect('track_complaint')

    
    return render(request, "edit_complaint.html", {'complaint': complaint})



from .models import Signin

def get_logged_in_user(request):
    username = request.session.get('user')  # Retrieve the username from the session
    if username:
        try:
            return Signin.objects.get(Username=username)
        except Signin.DoesNotExist:
            return None
    return None



def delete_complaint(request, complaint_id):
    if 'user' not in request.session:
        return redirect('login')  

    user = get_logged_in_user(request) 
    complaint = get_object_or_404(Complaint, id=complaint_id, user=user)  

    if request.method == "POST":
        complaint.delete() 
        messages.success(request, "Complaint deleted successfully.")
        return redirect('track_complaint')  

    return render(request, 'delete_complaint.html', {'complaint': complaint})


@login_required
def super_admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('error_page') 

    complaints = Complaint.objects.all()
    departments = Department.objects.all()
    categories = Category.objects.all()

    if request.method == "POST":
        if 'add_department' in request.POST:
            dept_name = request.POST.get('department_name')
            Department.objects.create(name=dept_name)
            messages.success(request, "Department added successfully!")
        elif 'delete_department' in request.POST:
            dept_id = request.POST.get('department_id')
            Department.objects.filter(id=dept_id).delete()
            messages.success(request, "Department deleted successfully!")
        elif 'add_category' in request.POST:
            cat_name = request.POST.get('category_name')
            Category.objects.create(name=cat_name)
            messages.success(request, "Category added successfully!")
        elif 'delete_category' in request.POST:
            cat_id = request.POST.get('category_id')
            Category.objects.filter(id=cat_id).delete()
            messages.success(request, "Category deleted successfully!")

    context = {
        "complaints": complaints,
        "departments": departments,
        "categories": categories,
    }
    return render(request, 'super_admin_dashboard.html', context)


@login_required
def view_complaint(request, complaint_id):
    
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    
    submitted_by = complaint.user  

    if request.method == "POST":
        
        complaint.status = "Verified"
        complaint.save()
        messages.success(request, "Complaint status updated to Verified.")

        user = Signin.objects.get(Username=request.session.get('user'))
        if user.is_super_admin:
            return redirect('super_admin_dashboard')  
        elif user.is_admin:
            return redirect('admin_dashboard')  

    return render(request, 'view_complaint.html', {'complaint': complaint, 'submitted_by': submitted_by})




@login_required
def user_dashboard(request):
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {'complaints': complaints})

# Error Page
def error_page(request):
    return render(request, 'error_page.html')


@login_required
def admin_dashboard(request):
    if 'user' not in request.session:  
        return redirect('login')  
    try:
        user = Signin.objects.get(Username=request.session['user'])
    except Signin.DoesNotExist:
        return redirect('login')  

    if not user.is_admin:  
        return redirect('error_page') 

    department_id = user.department.id if user.department else None
    complaints = Complaint.objects.filter(department_id=department_id).order_by('-created_at') if department_id else []

    return render(request, 'admin_dashboard.html', {'complaints': complaints})
