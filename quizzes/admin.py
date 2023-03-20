from django.contrib import admin
from .models import Question, Options, Answer

class OptionsInline(admin.TabularInline):
    model = Options
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionsInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
