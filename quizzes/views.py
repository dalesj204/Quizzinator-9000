from django.shortcuts import render, get_object_or_404
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
from .models import Class,  Grade, Stats, Question, Tag, Type, Quiz, User, Student, Teacher
from .decorators import user_is_teacher, user_is_student
from django.utils.decorators import method_decorator
import tablib
from django.urls import reverse
from tablib import Dataset
from .authentication import EmailAuthenticateBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone
import datetime
from datetime import datetime
import random
from django.db.models import Q
import re
# Create your views here.

# The home page displays a list of classes that the user is a part of
@login_required(login_url='login')
def index(request):
    this_user = User.objects.get(id=request.user.id)
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
    else:
        return redirect(LoginView)
    

def isActiveQuiz(now, start, end):
    return start < now and now < end


# Displays information about a class to a student/teacher
@login_required(login_url='login')
def ClassDetailView(request, class_id):
    this_user = User.objects.get(id=request.user.id)
    if this_user.is_student:
        student = Student.objects.get(user=this_user)
        try:
            this_class = student.classes.get(pk=class_id) 
            time = timezone.now()
            active_quizzes = []
            for q in this_class.quizzes.all():
                active_quizzes.append(isActiveQuiz(time, q.start_time, q.end_time))
                
            teacher_list = Teacher.objects.all()
            teachers_in_class = []
            for t in teacher_list:
                if t.classes.filter(pk=class_id).count() == 1:
                    teachers_in_class.append(t)
            context = {
                'user': student,
                'class': this_class,
                'current_time': time,
                'teacher_list': teachers_in_class,
                'quiz_info': zip(active_quizzes, this_class.quizzes.all()),
            }
            return render(request, 'class_detail_student.html', context=context)
        except:
            return render(request, 'not_in_class.html')
    elif this_user.is_teacher:
        teacher = Teacher.objects.get(user=this_user)
        try:
            this_class = teacher.classes.get(pk=class_id)
            student_list = Student.objects.all()
            students_in_class = []
            for s in student_list:
                if s.classes.filter(pk=class_id).count() == 1:
                    students_in_class.append(s)
                    
            teacher_list = Teacher.objects.all()
            teachers_in_class = []
            for t in teacher_list:
                if t.classes.filter(pk=class_id).count() == 1:
                    teachers_in_class.append(t)
            
            time = timezone.now()
            active_quizzes = []
            for q in this_class.quizzes.all():
                active_quizzes.append(isActiveQuiz(time, q.start_time, q.end_time))
            context = {
                'user': teacher,
                'class': this_class,
                'current_time': time,
                'student_list': students_in_class,
                'teacher_list': teachers_in_class,
                'quiz_info': zip(active_quizzes, this_class.quizzes.all()),
            }
            return render(request, 'class_detail_teacher.html', context=context)
        except:
            return render(request, 'not_in_class.html')

#Lists out all the students currently in the class and all of the other students in the databes into two tables
#precondition - n/a
#postcondition - you add or remove students from class
#parameter - class id, list of students associated and not associated with class
@login_required(login_url='login')
@user_is_teacher
def studentPageView(request, id):
        list2 =[]
        stud2 = Student.objects.all().filter(~Q(classes = id))
        for s in stud2:
            list2.append(User.objects.get(id=s.user.id))
        stud = Student.objects.all().filter(classes = id)
        list = []
        for s in stud:
            list.append(User.objects.get(id=s.user_id))
        template = loader.get_template('addStudent.html')
        context = {
            'student_list': list,
            'student_list_not_class': list2,
            'class_id': id,
        }
        return HttpResponse(template.render(context, request))

#This allows the teacher to select student in the database to be added to the class
#precondition - student must not already be in the class
#postcondition - student is now added to the class
#parameter - class id, list of students to be added to the class
@login_required(login_url='login')
@user_is_teacher
def addStudentrecord(request, id):
    if request.method == 'POST': 
        selectedStudent = request.POST.getlist('selectedStudent')
        for studentID in selectedStudent:
            stud = User.objects.get(id = studentID)
            stud2 = Student.objects.get(user = stud)
            stud2.classes.add(Class.objects.get(pk = id))
            stud.save()

    #Returns file for the response
    return HttpResponseRedirect(reverse('addStudent', args = [id]))

#this allows the teacher to remove a student from a class
#precondition - student must be already be in the class
#postcondition - student is now removed from the class
#parameter - class id, list of students to be removed from the class
@login_required(login_url='login')
@user_is_teacher
def deleteStudentrecord(request, id):
    if request.method == 'POST': 
        selectedStudent = request.POST.getlist('selectedStudent2')
        for studentID in selectedStudent:
            stud = User.objects.get(id = studentID)
            stud2 = Student.objects.get(user = stud)
            stud2.classes.remove(Class.objects.get(pk = id))
            stud.save()
    #Returns file for the response
    return HttpResponseRedirect(reverse('addStudent', args = [id]))

class ClassGradebookView(generic.ListView):
    model = Grade
    template_name = 'gradebook.html'


class ClassStatsView(generic.ListView):
    model = Stats
    template_name = 'stats.html'

# Just  displays the questions, has a spot to import new ones, enter new question manually, delete questions and export the questions.
# Returns a list of all questions in database 
#precondition - must be a teacher to view page
#parameter - list of question objects
#post condition - lists out all the questions with ability to add, delete, edit questions from database
class questionPageView(generic.ListView):
        model = Question
        template_name = 'questionPage.html'
        def get_context_data(self, **kwargs):
            ctx = super(questionPageView, self).get_context_data(**kwargs)
            ctx['ques'] = Question.objects.all()
            return ctx
        def index(request):
            template = loader.get_template('questionPage.html')
            temp = ["MC", "PMC", "PP"]
            return HttpResponse(template.render(request, temp))

  

#Creates a microsoft Excel sheet that contains all the selected questions(user can now select individual questions or all questions) from the database
#and their attributes including the question, correct answer, distractors, hint, and tags
# Precondition - none
# Parameter - none
# Postcondition - Questions/IDs and options/answers get exported to excel file named filename
    #Fills out the header with column names for each attribute
@login_required(login_url='login')
@user_is_teacher
def export_xcl(request):
     #Creates Excel workbook
    response = HttpResponse(content_type = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=filename.xls'
    file = xlwt.Workbook(encoding="utf-8")
    #Creates Excel sheet apart of the workbook
    filesheet = file.add_sheet("Questions")
    row_number = 0
    #Fills out the header with column names for each attribute
    columns = ['ID', 'Question' , 'Type','Answer', 'Options', 'Hint', 'Tags']
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
            leng = row.tag.all().count()
            con = 1
            for k in row.tag.all():
                    if con != 1 and con < leng + 1:
                        tempTwo = tempTwo + '|' + str(k.tag)
                        con = con + 1
                    else:
                        tempTwo = tempTwo + str(k.tag) + ''
                        con = con + 1
            #resultStringTwo = '|'.join(tempTwo)
            #puts each attribute for each question in corresponding cell
            for col_num in range(len(columns)):
                if col_num == 0:
                    filesheet.write(row_number, col_num, row.id)
                elif col_num == 1:
                    filesheet.write(row_number, col_num, row.stem)
                elif col_num == 2:
                    filesheet.write(row_number, col_num, row.type)
                    # if row.type == 0:
                    #     filesheet.write(row_number, col_num, 'MC')
                    # elif row.type == 1:
                    #     filesheet.write(row_number, col_num, 'PMC')
                    # elif row.type == 2:
                    #     filesheet.write(row_number, col_num, 'PP')
                elif col_num == 3:
                    tempthree = []
                    tempf = 0
                    con2 = 1
                    leng2 = row.options.all().count()
                    con2 = 1
                    for x in row.correctOption.all():
                        if con2 != 1 and con2 < leng2 + 1:
                            print("inhere3")
                            tempthree.append('|')
                            tempthree.append(x.content)
                            print(row.type)
                            if row.type == 1:
                                print("inhere")
                                tempthree.append(':@')
                                tempthree.append(str(x.orderForPerm))
                            con2 = con2 + 1
                        else:
                            print("inhere4")
                            print(row.type)
                            tempthree.append(x.content)
                            if row.type == 1:
                                print("inhere2")
                                tempthree.append(':@')
                                tempthree.append(str(x.orderForPerm))
                            con2 = con2 + 1
                    filesheet.write(row_number, col_num, tempthree)
                elif col_num == 4:
                    tempthree = []
                    tempf = 0
                    leng2 = row.options.all().count()
                    con2 = 1
                    for x in row.options.all():
                        if con2 != 1 and con2 < leng2 + 1:
                            tempthree.append('|')
                            tempthree.append(x.content)
                            con2 = con2 + 1
                        else:
                            tempthree.append(x.content)
                            con2 = con2 + 1
                    filesheet.write(row_number, col_num, tempthree)
                elif col_num == 5:
                    filesheet.write(row_number, col_num, row.explain)
                elif col_num == 6:
                    filesheet.write(row_number, col_num, tempTwo)
                
    file.save(response)
    #Returns file for the response
    return response

#Import form gives a form/template to give the file/filename that you will be importing
@login_required(login_url='login')
@user_is_teacher
def importing(request):
    template = loader.get_template('import_form.html')
    return HttpResponse(template.render({}, request))

#takes a microsoft Excel sheet that contains  questions that will go into the database
#and their attributes including the question, correct answer, distractors,answer, option hint, and tags
# Warning - if you use an ID already in the question bank you will overwrite the question
# Precondition - must be given an excel sheet, no other files
# Parameter - root(question), correct_answer, distractors, hint, tags (all in the excel sheet)
# Postcondition - Questions/IDs and options/answers now exists in the database with the correct fields
@login_required(login_url='login')
@user_is_teacher
def import_xcl(request):
    try:
        dataset = tablib.Dataset()
        new_questions = request.FILES['my_file']
        imported_data = dataset.load(new_questions.read(), format = 'xls')
        for data in imported_data:
            temp = []
            for tag in data[6].split('|'): # tag
                if not Tag.objects.all().filter(tag=tag).exists():
                    h = Tag(tag = tag)
                    h.save()
                else:
                    h= Tag.objects.get(tag=tag)
                temp.append(h)
            
            value = Question(
                id = data[0], # id
                stem = data[1], # stem
                type = data[2], # type
                explain = data[5], # explain
            )
            value.save()
            value.tag.add(*temp)
            value.save()
            ansList = []
            for ans in data[3].split('|'):
                if data[2] == 1:
                    listOrder = ans.split(':@')
                    order = listOrder[1]
                    cont = listOrder[0]
                    if(not(Options.objects.all().filter(content = cont, orderForPerm = order).exists())):
                        if data[2] == 1:
                            print(cont)
                            o = Options(content = cont, orderForPerm = order)
                            o.save()
                    ansList.append(Options.objects.get(content=cont, orderForPerm = order).id)
                else:
                    if(not(Options.objects.all().filter(content = ans, orderForPerm = 0).exists())):
                        o = Options(content = ans, orderForPerm = 0)
                        o.save()
                    ansList.append(Options.objects.get(content=ans, orderForPerm = 0).id)
            value.correctOption.set(ansList)
            optionList = []
            for op in data[4].split('|'):
                if not Options.objects.all().filter(content=op, orderForPerm = 0).exists():
                    h = Options(content=op, orderForPerm = 0)
                    h.save()
                optionList.append(Options.objects.get(content=op, orderForPerm = 0).id)
            value.options.set(optionList)
            
                
        return HttpResponseRedirect(reverse('questionPage'))
    except:
        messages.error(request, "File must be an excel file", extra_tags='excel')
        return HttpResponseRedirect(reverse('importing'))
    
# go back to the blog detail page after comment has been posted
@login_required(login_url='login')
@user_is_teacher
def get_success_url(self):
    return reverse('questionPage')

  
#Takes you to a page to fill out the fields to create a question manually 
@login_required(login_url='login')
@user_is_teacher
def add(request):
    template = loader.get_template('add.html')
    return HttpResponse(template.render({}, request))


# Function takes your fields and and allows users to add more questions while saving them to the database, 
# cancel their question(doesn't add it to the data base), or save question to the database and return to the questions page
# Precondition - Every field except for the hint has to be filled in
# Parameter - root(question), correct_answer, distractors, hint, tags
# Postcondition - Question/ID now exists in the database with the correct fields
@login_required(login_url='login')
@user_is_teacher
def addrecord(request):
    x = request.POST['stem']
    y = request.POST['type']
    z = request.POST['explain']
    q = request.POST['tag']
    o = request.POST['options']
    c = request.POST['correctOption']
    if(not Question.objects.all().filter(stem=x).exists()):
        ques = Question(stem=x, type=y, explain=z)
        ques.save()
        if 'Submit' in request.POST:
            temp = []
            for k in q.split('|'):
                h = Tag(tag = k)
                h.save()
                temp.append(h)
            ques.tag.add(*temp)
            ansList = []
            for x in c.split('|'):
                if y == '1':
                    listOrder = x.split(':@')
                    order = listOrder[1]
                    cont = listOrder[0]
                    if(not(Options.objects.all().filter(content = cont, orderForPerm = order).exists())):
                            if y == '1':
                                ans = Options(content = cont, orderForPerm = order)
                                ans.save()
                    ansList.append(Options.objects.get(content=cont, orderForPerm = order).id)
                else:
                    if(not(Options.objects.all().filter(content = x, orderForPerm = 0).exists())):
                        ans = Options(content = x)
                        ans.save()
                    ansList.append(Options.objects.get(content=x, orderForPerm = 0).id)
            ques.correctOption.set(ansList)
            optionList = []
            for x in o.split('|'):
                if y == '1':
                    cont = re.sub(r':@[0-9]', '', x)
                    if(not(Options.objects.all().filter(content = cont).exists())):
                        if y == '1':
                            ans = Options(content = cont)
                            ans.save()
                    optionList.append(Options.objects.get(content=cont).id)
                else:
                    if not Options.objects.all().filter(content=x).exists():
                        h = Options(content=x, orderForPerm=0)
                        h.save()
                    optionList.append(Options.objects.get(content=x).id)
            ques.options.set(optionList)
            ques.save()
            return HttpResponseRedirect(reverse('questionPage'))
        elif 'Cancel' in request.POST:
            return HttpResponseRedirect(reverse('questionPage'))
        else:
            temp = []
            for k in q.split('|'):
                h = Tag(tag = k)
                h.save()
                temp.append(h)
            ansList = []
            for x in c.split('|'):
                if y == '1':
                    listOrder = x.split(':@')
                    order = listOrder[1]
                    cont = listOrder[0]
                    if(not(Options.objects.all().filter(content = cont, orderForPerm = order).exists())):
                            if y == '1':
                                ans = Options(content = cont, orderForPerm = order)
                                ans.save()
                    ansList.append(Options.objects.get(content=cont, orderForPerm = order).id)
                else:
                    if(not(Options.objects.all().filter(content = x, orderForPerm = 0).exists())):
                        ans = Options(content = x)
                        ans.save()
                    ansList.append(Options.objects.get(content=x, orderForPerm = 0).id)
            ques.correctOption.set(ansList)
            optionList = []
            for x in o.split('|'):
                if not Options.objects.all().filter(content=x , orderForPerm = 0).exists():
                    h = Options(content=x)
                    h.save()
                optionList.append(Options.objects.get(content=x, orderForPerm = 0).id)
            ques.options.set(optionList)
            ques.tag.add(*temp)
            ques.save()
            return HttpResponseRedirect(reverse('add'))
    else: return HttpResponseRedirect(reverse('questionPage'))
    
# Function that deletes the question from the question bank. 
# And then returns you do the question page that should not have that question in the list anymore.
# Precondition - Question/ID must exist
# Parameter - Must be given question id to give
# Postcondition - Question/ID no longer exist/is not being used anymore
@login_required(login_url='login')
@user_is_teacher
def delete(request, id):
    ques = Question.objects.get(id=id)
    ques.delete()
    return HttpResponseRedirect(reverse('questionPage'))

# Function that edit the question from the question bank. 
# And then returns you do the question page that should have the updated question in the list. Unless they canceled it.
# Precondition - Question/ID must exist
# Parameter - Must be given question id to give
# Postcondition - Question is now updated
@login_required(login_url='login')
@user_is_teacher
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
     

# allows a user to register as a student
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


# allows a user to register as a teacher
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
    
    
# shows the options to register as either a student or a teacher
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
            messages.error(request, 'Invalid email or password.', extra_tags='login')
    form = LoginForm()
    return render(request, 'login.html', {'form' : form}) 


@login_required(login_url='login')
def LogoutView(request):
    logout(request)
    messages.info(request, "Logged out successfully.", extra_tags='logout')
    return redirect(index, permanent=True)


# QuizCreateView - Give the user the ability to create
# and instance of the quiz model.
#
# Author - Jacob Fielder
class QuizCreateView(View):
    def get(self, request):
        # Render the quiz creation form
        return render(request, 'quiz_create.html')

    def post(self, request):
        # Get the quiz details from the form
        quiz_name = request.POST['quiz_name']
        start_time_str = request.POST['start_time']
        end_time_str = request.POST['end_time']

        # Parse the datetime strings into datetime objects
        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')

        # Create a new quiz instance
        quiz = Quiz(name=quiz_name, start_time=start_time, end_time=end_time)

        # Convert the naive datetime objects to aware datetime objects
        quiz.start_time = timezone.make_aware(quiz.start_time, timezone.get_current_timezone())
        quiz.end_time = timezone.make_aware(quiz.end_time, timezone.get_current_timezone())

        quiz.save() # Save the quiz to the database to generate an ID
        self.process_question_selection(request, quiz)

        # Retrieve the questions that were added to the quiz
        questions = quiz.questions.all()

        # Render the quiz summary page with quiz details and selected questions
        return render(request, 'quiz_summary.html', {'quiz': quiz, 'questions': questions})

    def process_question_selection(self, request, quiz):
        if request.method == 'POST':
            # Get the selected questions from the form
            selected_question_ids = request.POST.getlist('question_ids[]')

            # Add selected questions to the quiz
            for question_id in selected_question_ids:
                question = Question.objects.get(id=question_id)
                quiz.questions.add(question)

# QuizList - Displays all quizzes in the database
#
# Author - Jacob Fielder
class QuizListView(View):
    def get(self, request):
        # Retrieve all quizzes from the database
        quizzes = Quiz.objects.all()

        # Render the quiz list page with quizzes
        return render(request, 'quiz_list.html', {'quizzes': quizzes})

    def post(self, request):
        # Retrieve quizzes based on search query
        query = request.POST['query']
        quizzes = Quiz.objects.filter(name__icontains=query)

        # Render the quiz list page with filtered quizzes
        return render(request, 'quiz_list.html', {'quizzes': quizzes})

# QuizSummaryView - Create a Summary of the Quiz after
# creation.
#
# Author - Jacob Fielder
class QuizSummaryView(View):
    def get(self, request, quiz_id):
        # Get the quiz instance from the database
        quiz = Quiz.objects.prefetch_related('questions').get(id=quiz_id)

        # Retrieve the questions that were added to the quiz
        questions = quiz.questions.all()

        # Render the quiz summary page with quiz details and selected questions
        return render(request, 'quiz_summary.html', {'quiz': quiz, 'questions': questions})

#As the user types in the question, perform a search.
def search_questions(request):
    stem = request.GET.get('stem', '')
    questions = Question.objects.filter(stem__icontains=stem)
    data = []
    for question in questions:
        data.append({
            'id': question.id,
            'stem': question.stem  # Include the 'stem' field in the JSON response
        })
    return JsonResponse(data, safe=False)


# A simple helper method for TakeQuizView
# 
# @param an array of the answers
# @return a randomized array of the same type
def randomizeAnswers(answers):
    new_array = [None for a in answers]
    for a in answers:
        temp = random.randint(0, len(answers) - 1)
        while not new_array[temp] == None:
            temp = random.randint(0, len(answers) - 1)
        new_array[temp] = a
    return new_array


# Renders the quiz with all answers in a random order
# 
# Constructs: "take_quiz.html"
# Reverse Name: "take_quiz"
# 
# Utilizes randomizeAnswers method defined above
# Has an optional "error" section to display misinputs on the user's end
@login_required(login_url='login')
@user_is_student
def TakeQuizView(request, quiz_id, error="none"):
    this_quiz = Quiz.objects.get(id=quiz_id)
    name = this_quiz.name
    questions = this_quiz.questions.all()
    for q in questions:
        q.order = (randomizeAnswers(q.options.all()))

    context = {
        'name': name,
        'questions': questions,
        'quiz_id': quiz_id,
        'error': error
    }
    return render(request, 'take_quiz.html', context=context)


# Post processing method for TakeQuizView
# 
# Constructs: "quiz_results.html"
# Reverse Name: "submitQuiz"
# 
# Recieves the submitted question IDs and proceses the grade
# 
# If the grade is sufficient, it creates a page with the
# grade visible and a return home button
# If the grade is insufficient, it makes the same page,
# but adds a retake quiz button
# 
# If the user inputs an incorrect amount of choices
# (ie. too many or too few) it redirects you back to
# the quiz so that you can retake it and submit the
# appropriate amount of answers
@login_required(login_url='login')
@user_is_student
def SubmitQuiz(request, quiz_id):
    if request.method == 'POST':
        # Declaration of variables
        selectedOpt = request.POST.getlist('selectedOpt')
        this_quiz = Quiz.objects.get(id=quiz_id)
        questions = this_quiz.questions.all()

        total_answers = 0
        for q in questions:
            total_answers+=q.correctOption.count()
        
        # Checks if the appropriate amount of answers were submitted
        if(not (len(selectedOpt) == total_answers)):
            # KNOW BUG: The url of the reroute will be the
            # summary page, but display the quiz still
            return TakeQuizView(request, quiz_id, error="MMChoices")
        
        # Total answers correct
        # 
        # Because each question can only have one answer,
        # each selected option will correspond to exactly
        # one question in the exact order that they were
        # stored in the "questions" field of the Quiz model
        #
        # This means a for loop counter will always match
        # the choice to the appropriate question
        count = 0
        offset = 0
        for i in range(len(questions)):
            options = list(str(o.id) for o in questions[i].correctOption.all())
            flag = True
            for i in range(len(options)):
                # Compares correctOption *ID* with that question's answer's *ID*
                if(not options[i] == (selectedOpt[offset])):
                    flag = False
                offset+=1
            if(flag):
                count+=1

        # Quick score calculation and check against the passingThreshold
        score = count / len(questions)
        score = round(score * 100, 2)
        if(this_quiz.passingThreshold >= score):
            retake = True
        else:
            retake = False
        
        # The retake boolean is processed in the HTML page
        context = {
            "score": str(score) + "%",
            "questions": questions,
            "quiz": this_quiz,
            'retake': retake

        }
        return render(request, 'quiz_results.html', context=context)

