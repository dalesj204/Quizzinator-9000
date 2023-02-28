from django.contrib import admin
from .models import Quiz, Class, Grade, Teacher, Student, Stats, MultipleChoiceQuestion

# Register your models here.

admin.site.register(Quiz)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Stats)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(Class)
admin.site.register(Grade)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    fields = ['name', 'course']

class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'quiz', 'student', 'gradebook','instructor')
    fields = ['name', 'quiz', 'student', 'gradebook','instructor']

