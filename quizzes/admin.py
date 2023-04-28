from django.contrib import admin
from .models import Class, Stats, Quiz, Tag, Question, Options, Teacher, Student, User

admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Stats)
admin.site.register(Class)
admin.site.register(Options)
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Quiz)

class QuestionInline(admin.TabularInline):
    model = Question

class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'student', 'gradebook','instructor')
    fields = ['name', 'student', 'gradebook','instructor']

class OptionsInline(admin.TabularInline):
    model = Options
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionsInline]
    raw_id_fields = ('quiz',)
    list_display = ('__str__',)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'course')
    fields = ['name', 'course']
    inlines = [QuestionInline]
    raw_id_fields = ('questions',)