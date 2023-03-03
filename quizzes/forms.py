from django import forms

from .models import Quiz, MultipleChoice, PermutationMultipleChoice, ParsonsProblem


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'end_time', 'time_limit', 'multiple_choice', 'permutation_multiple_choice', 'parsons_problem']
        widgets = {
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class MultipleChoiceForm(forms.ModelForm):
    class Meta:
        model = MultipleChoice
        fields = ['question', 'correct_answer', 'distractor1', 'distractor2', 'distractor3']


class PermutationMultipleChoiceForm(forms.ModelForm):
    class Meta:
        model = PermutationMultipleChoice
        fields = ['question', 'choice1', 'choice2', 'choice3', 'choice4', 'correct_answers']


class ParsonsProblemForm(forms.ModelForm):
    class Meta:
        model = ParsonsProblem
        fields = ['question', 'code_segments', 'correct_answer']
