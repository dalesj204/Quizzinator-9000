from django.shortcuts import render
from django.http import HttpResponse
from quiz_home import models
from django.views import generic
from .models import Class, Student, Grade, Stats, Teacher
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    
    num_quizzes = 0#Quiz.objects.all().count()
    
    context = {
        'num_quizzes': num_quizzes,
    }
    
    return render(
        request,
        'index.html', context=context,
    )

def studentLogin(request):
    if request.method == 'POST':
        sid = request.POST.get('sid')
        password = request.POST.get('password')
        print("sid", sid, "password", password)
        student = models.Student.objects.get(sid=sid)
        print(student)
        
        if password == student.pwd:
            request.session['username']=sid
            request.session['is_login']=True 
            # paper = models.TestPaper.objects.filter(major=student.major)
            # grade = models.Record.objects.filter(sid=student.sid)

            return render(request, 'index.html', {'student': student, 'paper': paper, 'grade': grade})
        else:
            return render(request,'login.html',{'message':'Incorrect Password'})
    elif request.method == 'GET':
        return render(request, 'login.html')
    else:
        return HttpResponse("Plase use GET or POST method")


# Student Profile - Place Holder
#
#
#This is a place holder for the student profile view to have the
#profile page up and running. It is not complex as it only
#contains one field. Afterwards it returns render.
#
# @return render - Renders the student profile.
#@login_required
def studentProfile(request):
    name = Student.name #The name of the student
    #Context for render
    #NOTE- THIS WILL NEED TO CHANGE LATER.
    context = {'name': name}
    return render(request, 'profile.html', context)

class ClassListView(generic.ListView):
    model = Class
    paginated_by = 10
    template_name = 'class_list.html'


class ClassGradebookView(generic.ListView):
    model = Grade
    template_name = 'gradebook.html'


class ClassStatsView(generic.ListView):
    model = Stats
    template_name = 'stats.html'

def TeacherHomeView(request, teacher_id):
    teacher = Teacher.objects.get(tid=teacher_id)
    classes = teacher.classes.all()

    context = {
        'teacher': teacher,
        'classes': classes,
    }

    return render(request, 'teacher_home.html', context)

def StudentHomeView(request, student_id):
    student = Student.objects.get(sid=student_id)
    classes = student.classes.all()

    context = {
        'student': student,
        'classes': classes,
    }

    return render(request, 'student_home.html', context)

def ClassDetailView(request, class_id):
    this_class = Class.objects.get(id=class_id)
    instructor = Teacher.objects.filter(classes=this_class)
    roster = Student.objects.filter(classes=this_class)

    context = {
        'class': this_class,
        'instructor': instructor,
        'roster': roster,
    }

    return render(request, 'class_detail.html', context)