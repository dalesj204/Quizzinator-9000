from django.contrib import admin
from .models import Class, Grade, Teacher, Student, Stats, fakeMultipleChoiceQuestion,  fakeDistractors, fakeSubjectTags

# Register your models here.

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Stats)
admin.site.register(Class)
admin.site.register(Grade)
admin.site.register(fakeMultipleChoiceQuestion)
admin.site.register(fakeDistractors)
admin.site.register(fakeSubjectTags)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    fields = ['name', 'course']

class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'student', 'gradebook','instructor')
    fields = ['name', 'student', 'gradebook','instructor']

