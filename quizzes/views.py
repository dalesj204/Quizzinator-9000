from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseBadRequest
from .models import Quiz, QuestionBank
from .forms import QuizForm, QuestionBankForm

# @login_required
# def create_quiz(request):
#     if request.method == 'POST':
#         form = QuizForm(request.POST)
#         if form.is_valid():
#             quiz = form.save(commit=False)
#             quiz.owner = request.user
#             quiz.save()
