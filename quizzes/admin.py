from django.contrib import admin
from .models import MultipleChoiceQuestion, PermutationalMultipleChoiceQuestion, ParsonsProblem

@admin.register(MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'root', 'correct_answer')
    search_fields = ('root', 'correct_answer')

@admin.register(PermutationalMultipleChoiceQuestion)
class PermutationalMultipleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'root1', 'correct_answer1', 'root2', 'correct_answer2')
    search_fields = ('root1', 'correct_answer1', 'root2', 'correct_answer2')

@admin.register(ParsonsProblem)
class ParsonsProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')
    search_fields = ('question',)
