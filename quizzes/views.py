from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import View, ListView, TemplateView
from .models import *

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
