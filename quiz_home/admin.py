from django.contrib import admin
from .models import Quiz, Class, Grade

# Register your models here.

admin.site.register(Quiz)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    fields = ['name', 'course']

admin.site.register(Class)

admin.site.register(Grade)