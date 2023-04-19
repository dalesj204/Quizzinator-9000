from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


# Author - Shawn Cai
# Define the options for the 'Type' field of the 'Question' model
Type = (
    (0, 'MC'),
    (1, 'PMC'),
    (2, 'PP')
)

# Author - Shawn Cai
# Define the options for the 'Option' field of the 'Options' and 'Answer' models
Option = (
    (1, 'A'),
    (2, 'B'),
    (3, 'C'),
    (4, 'D'),
    (5, 'E'),
    (6, 'F'),
    (7, 'G'),
    (8, 'H')
)

# Create the 'Tag' model
class Tag(models.Model):
    tag = models.CharField(max_length=30, verbose_name='tag')
    class Meta:
        db_table = 'tags'  # Define the database table name
        verbose_name = 'Tag'  # Define the verbose name for the model
    def tag_label_return(self, obj):
      return f"{obj.name}"
# Create the 'Question' model
# Author - Shawn Cai
class Question(models.Model):
    stem = models.CharField(max_length=1024, verbose_name='stem', blank=False, null=False)
    type = models.IntegerField(choices=Type, verbose_name='type')
    explain = models.CharField(max_length=512, verbose_name='explain', blank=False, null=False)
    tag = models.ManyToManyField(Tag, blank=True)
    def get_type(self, ind):
        return f"{Type[ind]}"
    
    class Meta:
        db_table = 'questions'  # Define the database table name
        verbose_name = 'Question'  # Define the verbose name for the model

# Create the 'Options' model
# Author - Shawn Cai
class Options(models.Model):
    options = models.IntegerField(choices=Option, verbose_name='options')
    content = models.CharField(max_length=256, verbose_name='content')
    question = models.ForeignKey('Question', on_delete=models.CASCADE)  # Define a foreign key relationship to the 'Question' model

    class Meta:
        db_table = 'options'  # Define the database table name
        verbose_name = 'Option'  # Define the verbose name for the model
        unique_together = ('question', 'content')  # Define a unique constraint for the combination of 'question' and 'content' fields
        ordering = ['options']  # Define the default ordering for the model

# Create the 'Answer' model
# Author - Shawn Cai
class Answer(models.Model):
    options = models.IntegerField(choices=Option, verbose_name='options')
    question = models.ForeignKey('question', on_delete=models.CASCADE)  # Define a foreign key relationship to the 'Question' model

    class Meta:
        db_table = 'answers'  # Define the database table name
        verbose_name = 'Answer'  # Define the verbose name for the model
        unique_together = ('question', 'options')  # Define a unique constraint for the combination of 'question' and 'options' fields
        ordering = ['options']  # Define the default ordering for the model

# Create the 'Quiz' model
# Author - Shawn Cai
class Quiz(models.Model):
    name = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    time_limit = models.DurationField(default=timedelta(minutes=30))
    
    class Meta:
        db_table = 'quizzes'  # Define the database table name
        verbose_name = 'Quiz'  # Define the verbose name for the model
# The models with fake in front are for Jordan and I to mess around with for the use of getting the import/export working
# while the questions/question bank reamins unchanged by us so that the others can finish
# Do not touch
# class fakeMultipleChoiceQuestion(models.Model):
#     id = models.AutoField(primary_key=True)
#     root =models.TextField(default="")
#     correct_answer = models.TextField(default="")
#     distractors = models.TextField(default="")
#     hint = models.TextField(blank=True, null=True)
#     tags =models.TextField(default="")
#     def __str__(self):
#         return self.root

# # quiz model contains name, course attributes, startDate, and endDate for quizzes
# # A list of Quizzes will be listed in order of endDate for quiz, so it displays the quizzes that will end first
# # @return str self.name - The quiz's name.
# # @return absolute_url quiz_detail - the detail view for that particular quiz
# class Quiz(models.Model):
#     # id = models.AutoField('ID',primary_key=True)
#     name = models.CharField(max_length=100)
#     course = models.CharField(max_length=100)
#     startDate = models.DateField(help_text="Set the date for when you want this quiz to open:", null=True)
#     endDate = models.DateField(help_text="Set the date for when you want this quiz to close:", blank = True, null=True)
#     class Meta:
#         verbose_name_plural = "quizzes"
#         ordering = ["-endDate"]

#     def __str__(self):
#         return str(self.name)

#     def get_absolute_url(self):
#         return reverse('quiz_detail', kwargs={'pk': self.pk})
    
    
    
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
    id = models.CharField("ID", max_length=12, primary_key=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    
    #returns the name of the user.
    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)

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

    classes = models.ManyToManyField(Class)

    #For referencing the model.
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def get_absolute_url(self):
        return reverse('student', kwargs={'student_id': self.user.id})
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Teacher_User", default=None)

    classes = models.ManyToManyField(Class)
    
    #For referencing the model.
    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    
    def get_absolute_url(self):
        return reverse('teacher', kwargs={'teacher_id': self.user.id})
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name