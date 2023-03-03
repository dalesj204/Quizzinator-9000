from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class SubjectTags(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MultipleChoice(models.Model):
    question = models.CharField(max_length=255)
    choice1 = models.CharField(max_length=255)
    choice2 = models.CharField(max_length=255)
    choice3 = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    
    def __str__(self):
        return self.question
    

class PermutationMultipleChoice(models.Model):
    question = models.CharField(max_length=255)
    choice1 = models.CharField(max_length=255)
    choice2 = models.CharField(max_length=255)
    choice3 = models.CharField(max_length=255)
    choice4 = models.CharField(max_length=255)
    correct_choices = models.ManyToManyField('self', symmetrical=False)
    
    def __str__(self):
        return self.question
    

class ParsonsProblem(models.Model):
    question = models.CharField(max_length=255)
    code = models.TextField()
    correct_answer = models.CharField(max_length=255)
    distractor1 = models.CharField(max_length=255)
    distractor2 = models.CharField(max_length=255)
    distractor3 = models.CharField(max_length=255)
    
    def __str__(self):
        return self.question
    

class Quiz(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    time_limit = models.IntegerField()
    questions = models.ManyToManyField('MultipleChoice', 'PermutationMultipleChoice', 'ParsonsProblem')
    
    def __str__(self):
        return self.name
