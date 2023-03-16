from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from random import randrange

from quiz_home.models import Student, Teacher, BaseUser

class StudentSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    id = randrange(111111111111, 999999999999)
    while(len(Student.objects.filter(sid=id)) != 0):
        id = randrange(111111111111, 999999999999)

    class Meta(UserCreationForm.Meta):
        model = BaseUser

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
    name = forms.CharField(max_length=100)
    id = randrange(111111111111, 999999999999)
    while(len(Teacher.objects.filter(sid=id)) != 0):
        id = randrange(111111111111, 999999999999)

    class Meta(UserCreationForm.Meta):
        model = BaseUser

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.name = self.name
        teacher.tid = self.id
        return user