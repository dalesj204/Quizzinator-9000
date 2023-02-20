from django.contrib import admin
from .models import Quiz

# Register your models here.

admin.site.register(Quiz)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    fields = ['name', 'course']