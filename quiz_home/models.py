from django.db import models
from django.urls import reverse
# Create your models here.

class Quiz(models.Model):
    # id = models.AutoField('ID',primary_key=True)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)


    def __str__(self):
        return str(self.name)

    # def get_absolute_url(self):
    #     return reverse('quiz_detail', kwargs={'pk': self.pk})