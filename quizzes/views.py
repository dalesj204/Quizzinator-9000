from django.shortcuts import render
from django.views import generic
from import_export import fields
from import_export.widgets import ManyToManyWidget
from quizzes import views
import xlwt
from django.shortcuts import redirect
from django.views.generic import CreateView,View, ListView, TemplateView
from django.contrib import messages
from .forms import  questionForm
from django.http import HttpResponse, request, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import Class,  Grade, Stats, Question, Tag, Type#, fakeMultipleChoiceQuestion
import tablib
from django.urls import reverse
from tablib import Dataset
# from .resources import fakeMultipleChoiceQuestionResource
from .models import *
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
    question_resource = Question()
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
def ClassDetailView(request, class_id):
    this_class = Class.objects.get(id=class_id)

    context = {
        'class': this_class,
    }

    return render(request, 'class_detail.html', context)



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
