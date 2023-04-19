from django.contrib import admin
from .models import Class, Grade, Stats, Quiz, Tag, Question, Options, Answer, Teacher, Student, User#, fakeMultipleChoiceQuestion

# Register your models here.

admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Quiz)
admin.site.register(Stats)
admin.site.register(Class)
admin.site.register(Grade)
admin.site.register(Options)
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
# admin.site.register(fakeMultipleChoiceQuestion)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    fields = ['name', 'course']

class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'student', 'gradebook','instructor')
    fields = ['name', 'student', 'gradebook','instructor']

class OptionsInline(admin.TabularInline):
    model = Options
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionsInline]

