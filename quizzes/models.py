from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class SubjectTags(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class QuestionBank(models.Model):
    QUESTION_TYPES = (
        ('mcq', 'Multiple Choice'),
        ('pmcq', 'Permutation Multiple Choice'),
        ('pp', "Parson's Problem")
    )

    question = models.CharField(max_length=500)
    question_type = models.CharField(max_length=4, choices=QUESTION_TYPES)
    correct_answer = models.CharField(max_length=500)
    distractor_1 = models.CharField(max_length=500)
    distractor_2 = models.CharField(max_length=500)
    distractor_3 = models.CharField(max_length=500)

    def __str__(self):
        return self.question

class Quiz(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    time_limit = models.PositiveIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    questions = models.ManyToManyField(QuestionBank, related_name='quizzes')

    def __str__(self):
        return self.name
