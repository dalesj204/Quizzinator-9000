from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from . import models
import random
from django.http import HttpResponse
from django.forms import ModelForm

from .models import fakeMultipleChoiceQuestion

# form to edit questions
class questionForm(ModelForm):
    class Meta:
        model = fakeMultipleChoiceQuestion
        fields = ('root', 'correct_answer', 'distractors', 'hint', 'tags')
  
        
