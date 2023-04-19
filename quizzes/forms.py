from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from . import models
import random
from django.http import HttpResponse
from django.forms import ModelForm

from .models import Question, User, Student, Teacher

# form to edit questions
class questionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('stem', 'type', 'explain', 'tag')

ids = []
# generates random unique id  
def unique_id():
    tempid = random.randint(111111111111, 999999999999)
    while tempid in ids:
        tempid = random.randint(111111111111, 999999999999)
    ids.append(tempid)
    return tempid
        
class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    email = forms.EmailField(label='Email', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=100)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, max_length=100)
    tempid = unique_id()
    

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")
    
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count() > 0:  
            raise forms.ValidationError("This Email Already Exists")  
        return email  
    
    def clean_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if not (password1 and password2):
            raise forms.ValidationError("You must confirm your password")
        elif (password1 != password2):
            raise forms.ValidationError("Your passwords do not match")
        return password2
        
    @transaction.atomic
    def save(self, commit=False):
        user = User(id=self.tempid, is_student=True, first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'], email=self.cleaned_data['email'], password=self.cleaned_data['password2'], username=self.cleaned_data['email'])
        user.save()
        student = Student(user=user)
        student.save()
        return user
    
class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    email = forms.EmailField(label='Email', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=100)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, max_length=100)    
    tempid = unique_id()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")
    
    
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count() > 0:  
            raise forms.ValidationError("This Email Already Exists")  
        return email  
    
    def clean_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if not (password1 and password2):
            raise forms.ValidationError("You must confirm your password")
        elif (password1 != password2):
            raise forms.ValidationError("Your passwords do not match")
        return password2
        
    @transaction.atomic
    def save(self, commit=False):
        user = User(id=self.tempid, is_teacher=True, first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'], email=self.cleaned_data['email'], password=self.cleaned_data['password2'], username=self.cleaned_data['email'])
        user.save()
        teacher = Teacher(user=user)
        teacher.save()
        return user
    
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ("Email", "Password")