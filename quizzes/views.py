from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from import_export import fields
from import_export.widgets import ManyToManyWidget
from quizzes import views
import xlwt
from django.shortcuts import redirect
from django.views.generic import CreateView,View, ListView, TemplateView, DetailView
from django.contrib import messages
from .forms import  questionForm, StudentSignUpForm, TeacherSignUpForm, LoginForm
from django.http import HttpResponse, request, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import Class,  Grade, Stats, Question, Tag, Type, Quiz #, fakeMultipleChoiceQuestion
from .decorators import user_is_teacher, user_is_student
from django.utils.decorators import method_decorator
import tablib
from django.urls import reverse
from tablib import Dataset
# from .resources import fakeMultipleChoiceQuestionResource
from .authentication import EmailAuthenticateBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone
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

def isActiveQuiz(now, start, end):
    return start < now and now < end
    

@login_required(login_url='login')
def ClassListView(request):
    this_user = User.objects.get(id=request.user.id)
    if this_user.is_student:
        student = Student.objects.get(user=this_user)
        class_list = student.classes.all()
        time = timezone.now()
        context = {
            'user': student,
            'classes': class_list,
            'current_time': time,
        }
        return render(request, 'class_list.html', context=context)
    elif this_user.is_teacher:
        teacher = Teacher.objects.get(user=this_user)
        class_list = teacher.classes.all()
        time = timezone.now()
        context = {
            'user': teacher,
            'classes': class_list,
            'current_time': time,
        }
        return render(request, 'class_list.html', context=context)


# def ClassDetailView(request, class_id):
#     this_class = Class.objects.get(id=class_id)
#     instructor = Teacher.objects.filter(classes=this_class)
#     roster = Student.objects.filter(classes=this_class)

#     context = {
#         'class': this_class,
#         'instructor': instructor,
#         'roster': roster,
#     }

#     return render(request, 'class_detail.html', context)

# @property
# def PastStartTime(self):
#     return timezone.now() >= self.start_time

@login_required(login_url='login')
def ClassDetailView(request, class_id):
    this_user = User.objects.get(id=request.user.id)
    if this_user.is_student:
        student = Student.objects.get(user=this_user)
        try:
            this_class = student.classes.get(pk=class_id) 
            time = timezone.now()
            active_quizzes = []
            for q in this_class.quizzes:
                active_quizzes.append(isActiveQuiz(time, q.start_time, q.end_time))
            context = {
                'user': student,
                'class': this_class,
                'current_time': time,
                'is_active': active_quizzes,
            }
            return render(request, 'class_detail_student.html', context=context)
        except:
            return render(request, 'not_in_class.html')
    elif this_user.is_teacher:
        teacher = Teacher.objects.get(user=this_user)
        try:
            this_class = teacher.classes.get(pk=class_id)
            time = timezone.now()
            context = {
                'user': teacher,
                'class': this_class,
                'current_time': time,
            }
            return render(request, 'class_detail_teacher.html', context=context)
        except:
            return render(request, 'not_in_class.html')
    
    


#class ClassListView(generic.ListView):
#    model = Class
#    paginated_by = 10
#    template_name = 'class_list.html'


#@login_required(login_url='login')
#class ClassDetailView(ListView, class_id):


class ClassGradebookView(generic.ListView):
    model = Grade
    template_name = 'gradebook.html'


class ClassStatsView(generic.ListView):
    model = Stats
    template_name = 'stats.html'

# Just  displays the questions, has a spot to import new ones, enter new question manually, delete questions and export the questions.
# Returns a list of all questions in database 
class questionPageView(generic.ListView):
    model = Question
    template_name = 'questionPage.html'
    def index(request):
        ques = Question.objects.all().values()
        template = loader.get_template('questionPage.html')
        temp = ["MC", "PMC", "PP"]
        context = {
            'question_list': ques,
        }
        return HttpResponse(template.render(context, request, temp))
  

#Creates a microsoft Excel sheet that contains all the selected questions(user can now select individual questions or all questions) from the database
#and their attributes including the question, correct answer, distractors, hint, and tags
#this is connected to our fake multiple choice question which we modeled after the MC question that was current at the time
#So that we didn't mess with the other team members model while they were updating it this sprint
#also only did MC because the other models did not exist yet.
# Precondition - none
# Parameter - none
# Postcondition - Questions/IDs get exported to excel file named filename
    #Fills out the header with column names for each attribute

   
def export_xcl(request):
     #Creates Excel workbook
    response = HttpResponse(content_type = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=filename.xls'
    file = xlwt.Workbook(encoding="utf-8")
    #Creates Excel sheet apart of the workbook
    filesheet = file.add_sheet("Questions")
    row_number = 0
    #Fills out the header with column names for each attribute
    columns = ['ID', 'Question' , 'Type', 'Hint', 'Tags']
    for col_num in range(len(columns)):
        filesheet.write(row_number, col_num, columns[col_num])

    if request.method == 'POST': 
        selectedQues = request.POST.getlist('selectedQues')
        # temp = .values_list('id','stem', 'type', 'explain', 'tag')
        #Fills in the rows (each row is one question, and each column is the attribute)
        for row in Question.objects.all().filter(id__in=selectedQues):
            row_number += 1
            temp = ''
            tempTwo = ''
            col_num = 0
            #puts all the tags into one string
            for k in row.tag.all():
                    tempTwo = tempTwo + str(k.tag) + ' '
            #puts each attribute for each question in corresponding cell
            for col_num in range(len(columns)):
                if col_num == 0:
                    filesheet.write(row_number, col_num, row.id)
                elif col_num == 1:
                    filesheet.write(row_number, col_num, row.stem)
                elif col_num == 2:
                    if row.type == 0:
                        filesheet.write(row_number, col_num, 'MC')
                    elif row.type == 1:
                        filesheet.write(row_number, col_num, 'PMC')
                    elif row.type == 2:
                        filesheet.write(row_number, col_num, 'PP')
                elif col_num == 3:
                    filesheet.write(row_number, col_num, row.explain)
                elif col_num == 4:
                    filesheet.write(row_number, col_num, tempTwo)
                
    file.save(response)
    #Returns file for the response
    return response
#Import form gives a form/template to give the file/filename that you will be importing
def importing(request):
    template = loader.get_template('import_form.html')
    return HttpResponse(template.render({}, request))

#takes a microsoft Excel sheet that contains  questions that will go into the database
#and their attributes including the question, correct answer, distractors, hint, and tags
#this is connected to our fake multiple choice question which we modeled after the MC question that was current at the time
#So that we didn't mess with the other team members model while they were updating it this sprint
#also only did MC because the other models did not exist yet.
# Warning - if you use an ID already in the question bank you will overwrite the question
# Precondition - must be given an excel sheet, no other files
# Parameter - root(question), correct_answer, distractors, hint, tags (all in the excel sheet)
# Postcondition - Questions/IDs now exists in the database with the correct fields
def import_xcl(request):
    dataset = tablib.Dataset()
    new_questions = request.FILES['my_file']
    imported_data = dataset.load(new_questions.read(), format = 'xls')
    for data in imported_data:
        temp = []
        for tag in data[4].split('|'):
            h = Tag(tag = tag)
            h.save()
            temp.append(h)
        value = Question(
            data[0],
            data[1], # stem
            data[2], # type
            data[3], # explain
        )
        value.save()
        value.tag.add(*temp)
        value.save()
    return HttpResponseRedirect(reverse('questionPage'))
    
# go back to the blog detail page after comment has been posted
def get_success_url(self):
    return reverse('questionPage')

  
#Takes you to a page to fill out the fields to create a question manually 
def add(request):
    template = loader.get_template('add.html')
    return HttpResponse(template.render({}, request))


# Function takes your fields and and allows users to add more questions while saving them to the database, 
# cancel their question(doesn't add it to the data base), or save question to the database and return to the questions page
# Precondition - Every field except for the hint has to be filled in
# Parameter - root(question), correct_answer, distractors, hint, tags
# Postcondition - Question/ID now exists in the database with the correct fields
def addrecord(request):
    x = request.POST['stem']
    y = request.POST['type']
    z = request.POST['explain']
    q = request.POST['tag']
    ques = Question(stem=x, type=y, explain=z)
    if 'Submit' in request.POST:
        ques.save()
        temp = []
        for k in q.split('|'):
            h = Tag(tag = k)
            h.save()
            temp.append(h)
        ques.tag.add(*temp)
        ques.save()
        return HttpResponseRedirect(reverse('questionPage'))
    elif 'Cancel' in request.POST:
        return HttpResponseRedirect(reverse('questionPage'))
    else:
        ques.save()
        temp = []
        for k in q.split('|'):
            h = Tag(tag = k)
            h.save()
            temp.append(h)
        ques.tag.add(*temp)
        ques.save()
        return HttpResponseRedirect(reverse('add'))
    
# Function that deletes the question from the question bank. 
# And then returns you do the question page that should not have that question in the list anymore.
# Precondition - Question/ID must exist
# Parameter - Must be given question id to give
# Postcondition - Question/ID no longer exist/is not being used anymore
def delete(request, id):
    ques = Question.objects.get(id=id)
    ques.delete()
    return HttpResponseRedirect(reverse('questionPage'))

# Function that edit the question from the question bank. 
# And then returns you do the question page that should have the updated question in the list. Unless they canceled it.
# Precondition - Question/ID must exist
# Parameter - Must be given question id to give
# Postcondition - Question is now updated
def edit(request, id):
    question = Question.objects.get(id=id)
    template = loader.get_template('edit_question.html')
    form = questionForm(request.POST or None, instance=question)
    if 'Update' in request.POST:
        if form.is_valid():
            form.save()
            return redirect('questionPage')
    if 'Cancel' in request.POST:
        return HttpResponseRedirect(reverse('questionPage'))
    return HttpResponse(template.render({'question':question, 'form':form}, request))



# Create QuestionView class to display questions
# Author - Shawn Cai
class QuestionView(ListView):
    template_name = 'Questions/index.html'
    model = Question

# Create QuestionAddView class to add questions
# Author - Shawn Cai
class QuestionAddView(TemplateView):
    template_name = 'Questions/question_add.html'
    def post(self, request):
        data = request.POST
        res = {'status': 0, 'msg': 'Success!'}
        try:
            subject = Question()
            subject.stem = data.get('stem')
            subject.explain = data.get('explain')
            subject.type = data.get('type')
            print(data.getlist('option'))
            print(data.getlist('content'))
            print(data.getlist('explain'))
            print(data.getlist('answer'))
            subject.save()
            for one in data.getlist('option'):
                options = Options()
                options.subject_id = subject.id

                options.options = one
                options.content = data.getlist('content')[int(one)-1]
                options.save()
            for one in data.getlist('answer'):
                answer = Answer()
                answer.subject_id = subject.id
                answer.options = one
                answer.save()
        except Exception as e:
            print(e)
            res = {'status': 1, 'msg': 'Failed'}
        return JsonResponse(res)

# Create QuestionUpdateView class to update questions
# Author - Shawn Cai
class QuestionUpdateView(View):
    def get(self, request):
        return render(request, 'Questions/question_update.html')

    def post(self, request):
        data = request.POST
        res = {'status': 0, 'msg': 'Success!'}
        try:
            Question = Question.objects.get(id=data.get('uid'))
            print(Question)
            Question.stem = data.get('stem')
            Question.explain = data.get('explain')
            Question.type = data.get('type')
            print(data.getlist('option'))
            print(data.getlist('content'))
            print(data.getlist('answer'))
            Question.save()
            Options.objects.filter(subject_id=data.get('uid')).delete()
            for one in data.getlist('option'):
                options = Options()
                options.subject_id = Question.id
                options.options = one
                options.content = data.getlist('content')[int(one)-1]
                options.save()
            Answer.objects.filter(subject_id=data.get('uid')).delete()
            for one in data.getlist('answer'):
                answer = Answer()
                answer.subject_id = Question.id
                answer.options = one
                answer.save()
        except Exception as e:
            print(e)
            res = {'status': 1, 'msg': 'Failed'}
        return JsonResponse(res)

# Create QuestionDeleteView class to delete questions
# Author - Shawn Cai
class QuestionDeleteView(View):
    def get(self, request):
        data = request.GET
        res = {'status': 0, 'msg': 'Success!'}
        try:
            Question.objects.get(id=data.get('id')).delete()
        except Exception as e:
            print(e)
            res = {'status': 1, 'msg': 'Failed'}
        return JsonResponse(res)


class QuizView(View):
    def get(self, request):
        ques_id = Question.objects.get


@login_required(login_url='login')
def TeacherHomeView(request):
    # checks for authentication
    if request.user.is_authenticated:
        this_user = User.objects.get(id=request.user.id)
        
        # checks to make sure the user is a student
        if this_user.is_teacher:
            teacher = Teacher.objects.get(user=this_user)
            classes = teacher.classes.all()
            name = this_user.__str__()

            context = {
                'teacher': teacher,
                'classes': classes,
                'name': name,
                'teacher_id': request.user.id,
            }

            return render(request, 'teacher_home.html', context)
        
        # redirects user to student home if they are a teacher instead
        elif this_user.is_student:
            return redirect(StudentHomeView, student_id=request.user.id)
            

@login_required(login_url='login')
def StudentHomeView(request):
    # checks for authentication
    if request.user.is_authenticated:
        this_user = User.objects.get(id=request.user.id)
        
        # checks to make sure the user is a student
        if this_user.is_student:
            student = Student.objects.get(user=this_user)
            classes = student.classes.all()
            name = this_user.__str__()

            context = {
                'student': student,
                'classes': classes,
                'name': name,
                'student_id': request.user.id,
            }

            return render(request, 'student_home.html', context)
        
        # redirects user to teacher home if they are a teacher instead
        elif this_user.is_teacher:
            return redirect(TeacherHomeView, teacher_id=request.user.id)
        
    
            




def StudentSignUpView(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            form.email_clean()
            form.clean_password()
            EmailAuthenticateBackend.authenticate(form, request, username=form.email_clean(), password=form.clean_password())
            user = form.save(commit=False)
            user.set_password(request.POST["password1"])
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(index, permanent=True)
    else:
        form = TeacherSignUpForm()
    return render(request, 'student_registration.html', {'form' : form})

    
def TeacherSignUpView(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            form.email_clean()
            form.clean_password()
            EmailAuthenticateBackend.authenticate(form, request, username=form.email_clean(), password=form.clean_password())
            user = form.save(commit=False)
            user.set_password(request.POST["password1"])
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(index, permanent=True)
    else:
        form = TeacherSignUpForm()
    return render(request, 'teacher_registration.html', {'form' : form})
    
def RegistrationView(request):
    return render(request, 'registration.html')

# allows a user to log in
def LoginView(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(index, permanent=True)
        else:
            messages.error(request, 'Invalid email or password.')
    form = LoginForm()
    return render(request, 'login.html', {'form' : form}) 


#@login_required
def LogoutView(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect(index, permanent=True)