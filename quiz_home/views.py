from django.shortcuts import render
from quiz_home import models
from django.views import generic
from import_export import fields
from import_export.widgets import ManyToManyWidget
from quizzes import views
from django.contrib.auth.decorators import login_required
import xlwt
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from .forms import StudentSignUpForm, TeacherSignUpForm
from django.http import HttpResponse, request, HttpResponseRedirect
from django.template import loader
from .models import Class, Student, Grade, Stats, Teacher,  fakeMultipleChoiceQuestion, User
import tablib
from django.urls import reverse
from tablib import Dataset
from .resources import fakeMultipleChoiceQuestionResource
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
    name = str(Student.first_name) + " " + str(Student.last_name) #The name of the student
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

#This for creating a place to enter questions manually one by one on the page instead of bulk importing - Not complete ignore
# class fakeMultQuestionCreate(LoginRequiredMixin, CreateView):
#     model = fakeMultipleChoiceQuestion
#     fields = ['root','correct_answer', 'distractors', 'hint', 'tags']
#     template_name ='multQuest.html'
#     def get_context_data(self, **kwargs):
#         context = super(fakeMultQuestionCreate,self ).get_context_data(**kwargs)
#         context['blog'] = get_object_or_404(BlogPost, pk = self.kwargs['pk'])
#         return context
#     def form_valid(self, form):
#         form.instance.userCom = self.request.user
#         form.instance.BlogPost = get_object_or_404(BlogPost, pk = self.kwargs['pk'])
#         return super(BlogCommentCreate, self).form_valid(form)
#     def get_success_url(self):
#         return reverse('blogpost-detail', kwargs={'pk' : self.kwargs['pk'],})

#Just to display list of all questions
class questionPageView(generic.ListView):
    model = fakeMultipleChoiceQuestion
    template_name = 'questionPage.html'
    def index(request):
        ques = fakeMultipleChoiceQuestion.objects.all().values()
        template = loader.get_template('questionPage.html')
        context = {
            'fakemultiplechoicequestion_list': ques,
        }
        return HttpResponse(template.render(context, request))
  

#Creates a microsoft Excel sheet that contains all the questions in the database
#and their attributes including the question, correct answer, distractors, hint, and tags
#this is connected to our fake multiple choice question which we modeled after the MC question that was current at the time
#So that we didn't mess with the other team members model while they were updating it this sprint
#also only did MC because the other models did not exist yet.
def export_xcl(request):
    #Creates Excel workbook
    response = HttpResponse(content_type = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=filename.xls'
    file = xlwt.Workbook(encoding="utf-8")
    #Creates Excel sheet apart of the workbook
    filesheet = file.add_sheet("Questions")
    row_number = 0
    #Fills out the header with column names for each attribute
    columns = ['ID','Question' , 'Correct Answer', 'Distractors', 'Hint', 'Tags']
    for col_num in range(len(columns)):
        filesheet.write(row_number, col_num, columns[col_num])

    temp = fakeMultipleChoiceQuestion.objects.values_list('id','root', 'correct_answer', 'distractors', 'hint', 'tags')
    #Fills in the rows (each row is one question, and each column is the attribute)
    for row in temp:
        row_number += 1
        col_num = 0
        for col_num in range(len(row)):
            filesheet.write(row_number, col_num, str(row[col_num]))
    file.save(response)
    #Returns file for the response
    return response
def importing(request):
    template = loader.get_template('import_form.html')
    return HttpResponse(template.render({}, request))
# for importing 
def import_xcl(request):
    question_resource = fakeMultipleChoiceQuestionResource()
    dataset = tablib.Dataset()
    new_questions = request.FILES['my_file']
    imported_data = dataset.load(new_questions.read(), format = 'xls')
    for data in imported_data:
        value = fakeMultipleChoiceQuestion(
            data[0], # fake id
            data[1], # root
            data[2], # answer
            data[3], # distractors
            data[4], # hint
            data[5],# tags
        )
        value.save()
    return HttpResponseRedirect(reverse('questionPage'))
    

def get_success_url(self):
    # go back to the blog detail page after comment has been posted
    return reverse('questionPage')

  
  
def add(request):
    template = loader.get_template('add.html')
    return HttpResponse(template.render({}, request))
def addrecord(request):
    x = request.POST['root']
    y = request.POST['correct_answer']
    z = request.POST['distractors']
    q = request.POST['hint']
    s = request.POST['tags']
    ques = fakeMultipleChoiceQuestion(root=x, correct_answer=y, distractors=z, hint=q, tags=s)
    if 'Submit' in request.POST:
        ques.save()
        return HttpResponseRedirect(reverse('questionPage'))
    elif 'Cancel' in request.POST:
        return HttpResponseRedirect(reverse('questionPage'))
    else:
        ques.save()
        return HttpResponseRedirect(reverse('add'))
# def delete(request, id):
#     ques = fakeMultipleChoiceQuestion.objects.get(id=id)
#     ques.delete()
#     return HttpResponseRedirect(reverse('questionPage'))
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



class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'student_registration.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('quiz_home/')
    
    
class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'teacher_registration.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('quiz_home/')