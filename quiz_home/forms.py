from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from random import randrange

from quiz_home.models import Student, Teacher, User

class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    tempid = randrange(111111111111, 999999999999)
    email = forms.EmailField(required=True)
    
    # Checks to see if ID already exists
    #while(len(User.objects.filter(id=tempid)) != 0):
    #    tempid = randrange(111111111111, 999999999999)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.name = self.name
        student.sid = self.id
        return user
    
class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    tempid = randrange(111111111111, 999999999999)
    email = forms.EmailField(required=True)
    
    # Checks to see if ID already exists
    #while(len(User.objects.filter(id=tempid)) != 0):
    #    tempid = randrange(111111111111, 999999999999)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.name = self.name
        teacher.tid = self.id
        return user