from django.db import models
from django.urls import reverse
# Create your models here.

# quiz model contains name and course attributes
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
    
class MultipleChoiceQuestion(models.Model):
    question_text = models.CharField(max_length=500)
    a = models.CharField(max_length=100)
    b = models.CharField(max_length=100)
    c = models.CharField(max_length=100)
    d = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)

    def __str__(self):
        return self.question_text
    
# More will be added as the program is fleshed out
# For now, just having a name will suffice
class Class(models.Model):

    name = models.CharField(max_length=100)
    gradebook = models.ForeignKey(Grade, on_delete=models.CASCADE, default=1)
    gradebook = models.ForeignKey(Grade, on_delete=models.CASCADE, default=1)
    quizzes = models.ManyToManyField(Quiz)
    class Meta:
        verbose_name_plural = "classes"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('class_detail', kwargs={'class_id': self.pk})

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
    
    name = models.CharField(max_length=100)
    tid = models.CharField('Teacher ID',max_length=12,primary_key=True)

    classes = models.ManyToManyField(Class)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('teacher', kwargs={'teacher_id': self.tid})

# QuestionBank Model - To Be Further Modified
#
#
#The Question Bank model is simplistic in its inital design
#due to multiple choice questions being the only type curr-
#ently completed. As more questions types are developed, this
#will grow in complexity.
class QuestionBank(models.Model):
    #Tags for the tags for specific questions in our bank.
    QUESTION_TYPE = (
      ('MC', 'Multiple Choice'),
      ('PP', 'Parsens Problem'),
      ('PMC', 'Permutation Problem'),
    )

    #Have the bank point towards the MC Model
    questions = (
        ('MC', models.ForeignKey(MultipleChoiceQuestion,
                on_delete=models.CASCADE)),
        #Next Question Type
    )


"""
class SubjectTags(models.Model):
    subject_name = model.CharField(max_length=100)

    def __str__(self):
        return self.name

class Questions(models.Model):
    question_type = model.ForeignKey(QuestionBank, on_delete=models.CASCADE, default=1)
    subject_tag = model.ManyToOne(SubjectTags)
    question = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('question', kwargs={'pk': self.pk})
"""
