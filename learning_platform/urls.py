from django.contrib import admin
from django.urls import include, path
from courses import views

urlpatterns = [
    path('admin/', admin.site.urls),            
    path('accounts/', include('django.contrib.auth.urls')),            
    path('', views.home, name='home'),
    path('register_student/', views.student_register, name='student_register'),
    path('register_faculty/', views.faculty_register, name='faculty_register'),
    path('login/', views.login_view, name='login'),
    path('student_dashboard/<str:name>/', views.student_dashboard, name='student_dashboard'),
    path('faculty_dashboard/<str:name>/', views.faculty_dashboard, name='faculty_dashboard'),
    path('course/<int:course_id>/order/', views.order_course, name='order_course'),
    path('order/<int:order_id>/<str:student>/payment/', views.payment, name='payment'),
    path('course/<int:course_id>/upload_topic/', views.upload_topic, name='upload_topic'),
    path('logout/', views.logout_view, name='logout'),
    path('add_courses/', views.add_courses, name='add_courses'),
    path('delete_course/<int:course_id>/<str:faculty>', views.delete_course, name='delete_course'),
    path('edit_course/<int:course_id>', views.edit_course, name='edit_course'),
    
]
