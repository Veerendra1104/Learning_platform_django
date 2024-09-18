from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse
from .forms import StudentSignUpForm, FacultySignUpForm, add_courses_form
from .models import Course, Order, Topic, User

def home(request):
    return render(request, 'home.html')

def student_register(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = StudentSignUpForm()
    return render(request, 'register.html', {'form': form})

def faculty_register(request):
    if request.method == 'POST':
        form = FacultySignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = FacultySignUpForm()
    return render(request, 'register.html', {'form': form})
from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         # users = User.objects.get(username = username)
#         # print(f"{username} and {users.username}, {password} and {users.password}")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             print("HIII")
#             login(request, user)
#             if user.is_student:
#                 return render(request,'student_dashboard')
#             else:
#               return render(request,'faculty_dashboard')
#         else:
#             return HttpResponse("Invalid username and password ")
#     return render(request, 'login.html')



@csrf_exempt
def login_view(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            # Authenticate the user
            user = User.objects.get(username = username)
            if username== user.username and password== user.password1:

                if user is not None:
                    # Successful authentication
                    login(request, user)

                    # Redirect based on user type
                    if hasattr(user, 'is_student') and user.is_student:
                        student_name = username
                        return redirect('student_dashboard', name=student_name)
                    else:
                        faculty_name = username  # Example, adjust based on your logic
                        return redirect('faculty_dashboard', name=faculty_name)
                else:
                    # Failed authentication
                    return HttpResponse("Invalid username and password")

        return render(request, 'login.html')


















    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
       
    #     users = User.objects.get(username = username)
    #     if username== users.username and password== users.password1:
    #     # if user is not None:
    #     #     print("Authentication successful")
    #     #     login(request, user)

    #         # Redirect based on user type
    #         if users.is_student:
    #             redirect('student_dashboard')
    #         else:
    #             faculty_name = username  # Example, you should get this dynamically
    #             return redirect('faculty_dashboard', name=faculty_name)
    #     else:
    #         print("Authentication failed")
    #         return HttpResponse("Invalid username and password")

    # return render(request, 'login.html')



from django.contrib.auth.decorators import login_required

@login_required
def student_dashboard(request, name):
    Courses = Course.objects.all()
    # for course in Courses:
    #     print(course)
    user = User.objects.get(username = name)
    orders = Order.objects.filter(student=user.pk)
    # orders = request.user.orders.all()
    return render(request, 'student_dashboard.html', {'courses': Courses ,'orders': orders })



@login_required
def faculty_dashboard(request, name):
      
    if request.method == 'POST':

        form = add_courses_form(request.POST)
        if form.is_valid():
            course_added = form.save()
            courses = Course.objects.get(faculty=name)
            # print(f'{courses.name}')
            return render(request, 'faculty_dashboard.html', {'courses': courses})
    else:
        courses = Course.objects.filter(faculty=name)
        if courses.exists():
            
            return render(request, 'faculty_dashboard.html', {'courses': courses})
        else:
            return render(request, 'faculty_dashboard.html', {'message': "You have no courses registered!"})


    # Example logic to retrieve courses or other information related to the faculty
 
@login_required
def order_course(request, course_id):
    # course_id = Course.objects.filter(name=course_name)
    course = Course.objects.get(id=course_id)
    order = Order.objects.create(student=request.user, course=course, amount=course.fees, payment_status=False)
    return redirect('payment', order_id=order.id, student=request.user )

@login_required
def payment(request, order_id, student):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        # Simulate payment process
        order.payment_status = True
        order.save()
        return redirect('student_dashboard', name=student )
    return render(request, 'payment.html', {'order': order})


@login_required
def upload_topic(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Topic.objects.create(course=course, title=title, content=content, uploaded_by=request.user)
        return redirect('faculty_dashboard')
    return render(request, 'upload_topic.html', {'course': course})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')

('name', 'description', 'faculty')

def add_courses(request):
    if request.method == 'POST':
        name = request.POST['faculty']
        form = add_courses_form(request.POST)
        if form.is_valid():
            courses = form.save()
            return redirect('faculty_dashboard', name=name)
    else:
        form = add_courses_form()
        return render(request, 'add_courses.html', {'form': form})
      
def delete_course(request, course_id, faculty):
        course = Course.objects.get(id=course_id)
        Course.delete(course)
        courses = Course.objects.filter(faculty=faculty)
        if courses.exists():
            if courses.count() == 1:
                courses = [courses.first()]
            return render(request, 'faculty_dashboard.html', {'courses': courses})
        else:
            return render(request, 'faculty_dashboard.html', {'message': "You have no courses registered!"})

def edit_course(request, course_id):
    course = Course.objects.get(id = course_id)
    if request.method == 'POST':
        name = request.POST['faculty']
        form = add_courses_form(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('faculty_dashboard', name=name)
    else:
        form = add_courses_form()
        return render(request, 'edit_course.html', {'form': form , 'course' : course})
        
def detail_view(request, course_id):
    course = Course.objects.get(id = course_id)
    return render(request, 'course_detail.html', {'course': course})

    
