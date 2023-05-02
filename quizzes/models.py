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


# Create the 'Tag' model
class Tag(models.Model):
    tag = models.CharField(max_length=30, verbose_name='tag')
    class Meta:
        db_table = 'tags'  # Define the database table name
        verbose_name = 'Tag'  # Define the verbose name for the model
    def tag_label_return(self, obj):
      return f"{obj.name}"
    def __str__(self):
        return self.tag

# The Options model helps build a question
# 
# The model stores just a string
# This allows a fixture script to create it on startup
# The question stores this model in a ManyToManyField
# The correct answer is now determined in the Question model
#
# Author - Shawn Cai
# Revised - Hayden Dustin - 4/23/23
class Options(models.Model):
    # The text to be displayed describing the choice in the question
    content = models.CharField(max_length=256, verbose_name='content')
    #
    orderForPerm = models.IntegerField(verbose_name='order', blank=True, null=True, default = 0)
    class Meta:
        db_table = 'options'    # Define the database table name
        verbose_name = 'Option' # Define the verbose name for the model

    def __str__(self):
        return self.content

# The Question model builds a quiz
# 
# The model stores a lot of information, listed below in comments
# The field correctOption MUST ALWAYS be filled upon INITIAL creation of the model
# The field options MUST contain the option stored in correctOption as well
# There is only ONE correctOption that can be stored, meaning
# there cannot be a question with more than one correct answer
# 
# ###SCRIPTING###
# When creating the models in a script, create the options first
# 
# Author - Shawn Cai
# Revised - Hayden Dustin - 4/23/23
class Question(models.Model):

    # The question being asked
    stem = models.CharField(max_length=1024, verbose_name='stem', blank=False, null=False)

    # Determines multiple choice, parsons, etc.
    type = models.IntegerField(choices=Type, verbose_name='type')

    # A hint for the question
    explain = models.CharField(max_length=512, verbose_name='explain', blank=False, null=False)

    # A list of tags for searching for questions
    tag = models.ManyToManyField(Tag, blank=True)

    # A list of options assigned to the question
    options = models.ManyToManyField(Options, related_name="options")

    # The correct answer for the question
    correctOption = models.ManyToManyField(Options, related_name="correctOption")

    # An array used for calculating the random order of the options
    order = []
    def get_type(self, ind):
        return f"{Type[ind]}"
    
    class Meta:
        db_table = 'questions'      # Define the database table name
        verbose_name = 'Question'   # Define the verbose name for the model

    def __str__(self):
        return self.stem
    

# This is the main model for the program
# 
# This model also stores a lot of information, which is described in comments within
# All questions are displayed on the same page
# 
# ###SCRIPTING###
# When creating these models in a script, create the
# questions FIRST (Follow other scripting instructions as well)
# 
# 
# Author - Shawn Cai
# Revised - Hayden Dustin - 4/23/23
class Quiz(models.Model):

    # The quiz's title
    name = models.CharField(max_length=255)

    # The list of questions contained in the quiz
    questions = models.ManyToManyField(Question)

    # The time the quiz becomes available
    start_time = models.DateTimeField(default=timezone.now)

    # The time the quiz becomes unavailable
    end_time = models.DateTimeField(default=timezone.now)

    # The amount of time given from the first attempt before the quiz automatically closes
    time_limit = models.DurationField(default=timedelta(minutes=30))

    # The grade the student must match or exceed for the quiz to be considered passed
    passingThreshold = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        db_table = 'quizzes'    # Define the database table name
        verbose_name = 'Quiz'   # Define the verbose name for the model

    def __str__(self):
        return self.name #So I can grab the Quiz Name
    
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

# Student Model
#
# Only stores the classes as new information
# This model attaches to the User model as a base
# for all user information and functionality
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

# Teacher Model
#
# Only stores the classes as new information
# This model attaches to the User model as a base
# for all user information and functionality
#
# @return self.name - The teachers's name.
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