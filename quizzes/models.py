from django.db import models

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

# Create the 'Question' model
# Author - Shawn Cai
class Question(models.Model):
    stem = models.CharField(max_length=1024, verbose_name='stem', blank=False, null=False)
    type = models.IntegerField(choices=Type, verbose_name='type')
    explain = models.CharField(max_length=512, verbose_name='explain', blank=False, null=False)
 
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
