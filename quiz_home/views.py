from django.shortcuts import render
from django.http import HttpResponse
from quiz_home import models
from django.views import generic
from .models import Quiz

# Create your views here.
def index(request):
    return render(
        request,
        'index.html',
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

    
class QuizListView(generic.ListView):
    model = Quiz
    paginated_by = 10
    template_name = 'quiz_list.html'

