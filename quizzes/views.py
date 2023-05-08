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
from .forms import  questionForm, StudentSignUpForm, TeacherSignUpForm, LoginForm, PasswordResetForm, AdminPasswordResetForm
from django.http import HttpResponse, request, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import Class, Stats, Question, Tag, Type, Quiz, User, Student, Teacher
from .decorators import user_is_teacher, user_is_student
from django.utils.decorators import method_decorator
import tablib
from django.urls import reverse
from tablib import Dataset
from .authentication import EmailAuthenticateBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from django.utils import timezone
import datetime
from datetime import datetime
import random
from django.db.models import Q
# Create your views here.

# allows the teacher to toggle between student and teacher views
@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser, login_url="/login/")
def AdminViewToggle(request, view_id):
    if view_id == "student":
        User.objects.filter(id=request.user.id).update(is_student=True)
        User.objects.filter(id=request.user.id).update(is_teacher=False)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    if view_id == "teacher":
        User.objects.filter(id=request.user.id).update(is_student=False)
        User.objects.filter(id=request.user.id).update(is_teacher=True)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# The home page displays a list of classes that the user is a part of
@login_required(login_url='login')
def index(request):
    this_user = User.objects.get(id=request.user.id)
    if not this_user.is_superuser:
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
        else:
            return redirect(LoginView)
    
    if this_user.is_superuser:
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
        
        if this_user.is_student:
            teacher = Teacher.objects.get(user=this_user)
            classes = teacher.classes.all()
            name = this_user.__str__()

            context = {
                'student': teacher,
                'classes': classes,
                'name': name,
                'student_id': request.user.id,
            }

            return render(request, 'student_home.html', context)
    else:
        return redirect(LoginView)
    

def isActiveQuiz(now, start, end, threshold, grade):
    return start < now and now < end and threshold > grade
def teacherIsActiveQuiz(now, start, end):
    return start < now and now < end


# Displays information about a class to a student/teacher
@login_required(login_url='login')
def ClassDetailView(request, class_id):
    this_user = User.objects.get(id=request.user.id)
    if not this_user.is_superuser:
        if this_user.is_student:
            student = Student.objects.get(user=this_user)
            try:
                this_class = student.classes.get(pk=class_id) 
                time = timezone.now()
                active_quizzes = []
                inactive_quizzes = []
                grades = []
                for q in this_class.quizzes.all():
                    user_info = q.gradebook.student_data.get(student_id = student.user.id)
                    if(isActiveQuiz(time, q.start_time, q.end_time, q.passingThreshold, user_info.grade)):
                        active_quizzes.append(q)
                    else:
                        inactive_quizzes.append(q)
                        grades.append(user_info.grade)
                    
                teacher_list = Teacher.objects.all()
                teachers_in_class = []
                for t in teacher_list:
                    if t.classes.filter(pk=class_id).count() == 1:
                        teachers_in_class.append(t)
                context = {
                    'class': this_class,
                    'current_time': time,
                    'teacher_list': teachers_in_class,
                    'active_quizzes': active_quizzes,
                    'inactive_quizzes': zip(inactive_quizzes, grades)
                }
                return render(request, 'class_detail_student.html', context=context)
            except:
                return render(request, 'not_in_class.html')
    
    if this_user.is_superuser:
        if this_user.is_teacher:
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
                inactive_quizzes = []
                for q in this_class.quizzes.all():
                    if(teacherIsActiveQuiz(time, q.start_time, q.end_time)):
                        active_quizzes.append(q)
                    else:
                        inactive_quizzes.append(q)
                context = {
                    'class': this_class,
                    'current_time': time,
                    'student_list': students_in_class,
                    'teacher_list': teachers_in_class,
                    'active_quizzes': active_quizzes,
                    'inactive_quizzes': inactive_quizzes
                }
                return render(request, 'class_detail_teacher.html', context=context)
            except:
                return render(request, 'not_in_class.html')
            
        if this_user.is_student:
            student = Teacher.objects.get(user=this_user)
            try:
                this_class = student.classes.get(pk=class_id) 
                time = timezone.now()
                active_quizzes = []
                inactive_quizzes = []
                grades = []
                for q in this_class.quizzes.all():
                    if(teacherIsActiveQuiz(time, q.start_time, q.end_time)):
                        active_quizzes.append(q)
                    else:
                        inactive_quizzes.append(q)
                        grades.append(0)
                    
                teacher_list = Teacher.objects.all()
                teachers_in_class = []
                for t in teacher_list:
                    if t.classes.filter(pk=class_id).count() == 1:
                        teachers_in_class.append(t)
                context = {
                    'class': this_class,
                    'current_time': time,
                    'teacher_list': teachers_in_class,
                    'active_quizzes': active_quizzes,
                    'inactive_quizzes': zip(inactive_quizzes, grades)
                }
                return render(request, 'class_detail_student.html', context=context)
            except:
                return render(request, 'not_in_class.html')

@login_required(login_url='login')
@user_is_teacher
def TeacherGradebookView(request, quiz_id):
    this_quiz = Quiz.objects.get(id = quiz_id)
    gb = this_quiz.gradebook.student_data.all()
    average = 0
    students = []
    for student in gb:
        students.append(Student.objects.get(user__id = student.student_id))
        average+= student.grade
    average = round(average / gb.count(), 2)
    context = {
        'quiz': this_quiz,
        'gradebook': zip(gb, students),
        'average': average
    }
    return render(request, 'gradebook.html', context)

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
            for c in stud2.classes.all():
                for q in c.quizzes.all():
                    q.populate(c.id)

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
            for c in stud2.classes.all():
                for q in c.quizzes.all():
                    q.populate(c.id)

    #Returns file for the response
    return HttpResponseRedirect(reverse('addStudent', args = [id]))

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
                    filesheet.write(row_number, col_num, row.correctOption.content)
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
            
            if(not(Options.objects.all().filter(content = data[3]).exists())):
                o = Options(content = data[3])
                o.save()
            o = Options.objects.get(content = data[3])
            value = Question(
                id = data[0], # id
                stem = data[1], # stem
                type = data[2], # type
                correctOption = o, # correctOption
                explain = data[5], # explain
            )
            value.save()
            value.tag.add(*temp)
            value.save()
            
            optionList = []
            for op in data[4].split('|'):
                if not Options.objects.all().filter(content=op).exists():
                    h = Options(content=op)
                    h.save()
                optionList.append(Options.objects.get(content=op).id)
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
        if not Options.objects.all().filter(content=c).exists():
            w = Options(content = c)
            w.save()
        c = Options.objects.get(content = c)
        ques = Question(stem=x, type=y, explain=z, correctOption = c)
        if 'Submit' in request.POST:
            ques.save()
            temp = []
            for k in q.split('|'):
                h = Tag(tag = k)
                h.save()
                temp.append(h)
            ques.tag.add(*temp)
            optionList = []
            for x in o.split('|'):
                if not Options.objects.all().filter(content=x).exists():
                    h = Options(content=x)
                    h.save()
                optionList.append(Options.objects.get(content=x).id)
            ques.options.set(optionList)
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
            optionList = []
            for x in o.split('|'):
                if not Options.objects.all().filter(content=x).exists():
                    h = Options(content=x)
                    h.save()
                optionList.append(Options.objects.get(content=x).id)
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
@login_required(login_url='login')
@user_is_teacher
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
            user.is_staff = True
            user.is_superuser = True
            user.save()
            return redirect(index, permanent=True)
    else:
        form = TeacherSignUpForm()
    return render(request, 'teacher_registration.html', {'form' : form})

# allows the user to change their password
@login_required(login_url='login')
def ChangePasswordView(request):
    this_user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.cleaned_data
            form.check_old_password(this_user=this_user)
            form.clean_password()
            this_user.set_password(request.POST["password1"])
            this_user.save()
            return redirect(index, permanent=True)
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form' : form})
                
            
@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser, login_url="/login/")
def AdminPasswordReset(request):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user_email = User.objects.filter(email=email)
        if user_email.count() == 1:  
            this_user = User.objects.get(email=email)
            if (password1 == password2):
                this_user.set_password(request.POST["password1"])
                this_user.save()
                return redirect(index, permanent=True)
            else:
                messages.error(request, 'Your passwords do not match', extra_tags='matchPassword')
        else:
            messages.error(request, 'This email does not exist', extra_tags='email')
    form = AdminPasswordResetForm()
    return render(request, 'admin_password_reset.html', {'form' : form})
    
# # shows the options to register as either a student or a teacher
# def RegistrationView(request):
#     return render(request, 'registration.html')

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
        classes = Class.objects.all()
        context = {
            'classes': classes
        }

        # Render the quiz creation form
        return render(request, 'quiz_create.html', context=context)

    def post(self, request):
        # Get the quiz details from the form
        quiz_name = request.POST['quiz_name']
        start_time_str = request.POST['start_time']
        end_time_str = request.POST['end_time']
        passingThreshold = request.POST['passingThreshold']
        class_ids = request.POST.getlist('selectedClass')

        # Parse the datetime strings into datetime objects
        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')

        # Create a new gradebook
        gb = Gradebook()
        gb.save()

        # Create a new quiz instance
        quiz = Quiz(name=quiz_name, start_time=start_time, end_time=end_time, gradebook = gb, passingThreshold = passingThreshold)

        # Convert the naive datetime objects to aware datetime objects
        quiz.start_time = timezone.make_aware(quiz.start_time, timezone.get_current_timezone())
        quiz.end_time = timezone.make_aware(quiz.end_time, timezone.get_current_timezone())

        quiz.save() # Save the quiz to the database to generate an ID
        self.process_question_selection(request, quiz)

        # Retrieve the questions that were added to the quiz
        questions = quiz.questions.all()

        for c in class_ids:
            this_class = Class.objects.get(id=c)
            quiz.populate(this_class.id)
            this_class.quizzes.add(quiz)

        quiz.save()
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

        # Checks if the appropriate amount of answers were submitted
        if(not (len(selectedOpt) == len(questions))):
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
        for i in range(len(questions)):
            # Compares correctOption *ID* with that question's answer's *ID*
            if(selectedOpt[i] == str(questions[i].correctOption.id)):
                count+=1
        # Quick score calculation and check against the passingThreshold
        score = count / len(questions)
        score = round(score * 100, 2)
        if(this_quiz.passingThreshold >= score):
            retake = True
        else:
            retake = False

        user_info = this_quiz.gradebook.student_data.get(student_id = request.user.id)
        if(user_info.grade < score):
            user_info.grade = score
        user_info.attempts+=1
        user_info.save()
        
        # The retake boolean is processed in the HTML page
        context = {
            "score": str(score) + "%",
            "questions": questions,
            "quiz": this_quiz,
            'retake': retake

        }
        return render(request, 'quiz_results.html', context=context)

