from django import forms
from .models import Quiz, QuestionBank


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'start_time', 'end_time', 'time_limit', 'questions']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'questions': forms.CheckboxSelectMultiple(),
        }


class QuestionBankForm(forms.ModelForm):
    class Meta:
        model = QuestionBank
        fields = ['question', 'question_type', 'correct_answer', 'distractor_1', 'distractor_2', 'distractor_3']
