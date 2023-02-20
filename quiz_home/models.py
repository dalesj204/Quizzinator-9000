from django.db import models
from django.urls import reverse
# Create your models here.

class Quiz(models.Model):
    # id = models.AutoField('ID',primary_key=True)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "quizzes"


    def __str__(self):
        return str(self.name)

    # def get_absolute_url(self):
    #     return reverse('quiz_detail', kwargs={'pk': self.pk})

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