from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Course

class StudentSignUpForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        return user

class FacultySignUpForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_faculty = True
        if commit:
            user.save()
        return user
  

class add_courses_form(forms.ModelForm):
    class Meta():
        model = Course
        fields = ('name', 'description', 'faculty','fees')
