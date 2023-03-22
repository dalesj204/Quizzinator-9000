from django.contrib import admin
from .models import  Tag, Question, Options, Answer, Quiz

class OptionsInline(admin.TabularInline):
    model = Options
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionsInline]

admin.site.register(Tag)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Quiz)
