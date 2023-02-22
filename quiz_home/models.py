from django.db import models
from django.urls import reverse
# Create your models here.

# quiz model contains name and course attributes
class Quiz(models.Model):
    # id = models.AutoField('ID',primary_key=True)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "quizzes"


    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('quiz_detail', kwargs={'pk': self.pk})

# More will be added as the program is fleshed out
# For now, just having a name will suffice
class Class(models.Model):

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "classes"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('class_detail', kwargs={'pk': self.pk})

# Student Model - Place Holder
#
#
#This is a place holder for the student model to have the
#profile page up and running. It is not complex as it only
#contains two fields. As the project continues, I implore
#you to edit this to the needs it program as it evolves.
#
# @return self.name - The student's name.
class Student(models.Model):
    #Fields.
    name = models.CharField(max_length=100)
    sid = models.CharField('Student ID',max_length=12,primary_key=True)

    #For referencing the model.
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    #returns the name of the user.
    def __str__(self):
        return self.name