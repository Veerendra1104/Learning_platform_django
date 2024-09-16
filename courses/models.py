from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.conf import settings


class User(AbstractUser):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='course_users', null=True)

    username = models.CharField(max_length=30, null=True, unique=True)
    email = models.EmailField()
    password1 = models.CharField(max_length=30, null=True)
    password2 = models.CharField(max_length=30, null=True)
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='courses_user_set',  # Update the related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='courses_user_set',  # Update the related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    faculty = models.CharField(max_length=30)
    fees = models.IntegerField(null=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    student = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, related_name='orders')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)

class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=255)
    content = models.TextField()
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title
