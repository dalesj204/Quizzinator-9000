from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from Quizinator import settings

# The models with fake in front are for Jordan and I to mess around with for the use of getting the import/export working
# while the questions/question bank reamins unchanged by us so that the others can finish
# Do not touch
class fakeSubjectTags(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return self.subject_name
    
class fakeDistractors(models.Model):
    subject_name = models.CharField(max_length=100)
    def __str__(self):
        return self.subject_name

class fakeMultipleChoiceQuestion(models.Model):
    root = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)
    distractors = models.ManyToManyField(fakeDistractors)
    hint = models.CharField(max_length=100, blank=True, null=True)
    tags = models.ManyToManyField(fakeSubjectTags)
    def __str__(self):
        return self.root

# quiz model contains name, course attributes, startDate, and endDate for quizzes
# A list of Quizzes will be listed in order of endDate for quiz, so it displays the quizzes that will end first
# @return str self.name - The quiz's name.
# @return absolute_url quiz_detail - the detail view for that particular quiz
class Quiz(models.Model):
    # id = models.AutoField('ID',primary_key=True)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    startDate = models.DateField(help_text="Set the date for when you want this quiz to open:", null=True)
    endDate = models.DateField(help_text="Set the date for when you want this quiz to close:", blank = True, null=True)
    class Meta:
        verbose_name_plural = "quizzes"
        ordering = ["-endDate"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('quiz_detail', kwargs={'pk': self.pk})
    
    
    
# temporary model for the sake of getting the gradebook page running.
class Grade(models.Model):
    name = models.CharField(max_length=100)
    grade = models.IntegerField()
    

    class Meta:
        verbose_name_plural = "grades"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('grade_list', kwargs={'pk': self.pk})
    

class Stats(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "stats"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('stat', kwargs={'pk': self.pk})
 
#This model has a name, there will be a gradebook associated for each user for each class,
#and each class can have many quizzes associated with it(every quiz can be assigned to many classes)
# @return str self.name - The class's name.
# @return absolute_url class_detail - the detail view for that particular class
class Class(models.Model):
    name = models.CharField(max_length=100)
    gradebook = models.ForeignKey(Grade, on_delete=models.CASCADE, default=1)
    quizzes = models.ManyToManyField(Quiz)
    class Meta:
        verbose_name_plural = "classes"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('class_detail', kwargs={'class_id': self.pk})


# Base User Model
# 
# This model is used to differentiate between the different
# levels of authorization between teachers and students
class User(AbstractUser):
    id = models.CharField("ID", max_length=12, primary_key=True, unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Student_User", default=None)
    sid = User(user).id
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    classes = models.ManyToManyField(Class)

    #For referencing the model.
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    #returns the name of the user.
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('student', kwargs={'student_id': self.sid})
    

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Teacher_User", default=None)
    tid = User(user).id
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    classes = models.ManyToManyField(Class)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('teacher', kwargs={'teacher_id': self.tid})