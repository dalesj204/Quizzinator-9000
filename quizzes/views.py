from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .models import Quiz, MultipleChoice, PermutationMultipleChoice, ParsonsProblem


def quiz_list(request):
    quizzes = Quiz.objects.filter(start_time__lte=timezone.now(), end_time__gte=timezone.now())
    return render(request, 'quiz_list.html', {'quizzes': quizzes})


@login_required
def create_quiz(request):
    if request.method == 'POST':
        name = request.POST['name']
        owner = request.user
        start_time = timezone.now()
        end_time = request.POST['end_time']
        time_limit = request.POST['time_limit']
        questions = request.POST.getlist('questions')
        
        quiz = Quiz(name=name, owner=owner, start_time=start_time, end_time=end_time, time_limit=time_limit)
        quiz.save()
        for question_id in questions:
            try:
                question = MultipleChoice.objects.get(id=question_id)
                quiz.questions.add(question)
            except ObjectDoesNotExist:
                try:
                    question = PermutationMultipleChoice.objects.get(id=question_id)
                    quiz.questions.add(question)
                except ObjectDoesNotExist:
                    try:
                        question = ParsonsProblem.objects.get(id=question_id)
                        quiz.questions.add(question)
                    except ObjectDoesNotExist:
                        pass
                
        return redirect('quiz_list')
    else:
        questions = {
            'multiple_choice': MultipleChoice.objects.all(),
            'permutation_multiple_choice': PermutationMultipleChoice.objects.all(),
            'parsons_problem': ParsonsProblem.objects.all
        }
    return render(request, 'create_quiz.html', {'questions': questions})

@login_required
def update_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        quiz.name = request.POST['name']
        quiz.end_time = request.POST['end_time']
        quiz.time_limit = request.POST['time_limit']
        quiz.questions.clear()
        questions = request.POST.getlist('questions')
        for question_id in questions:
            try:
                question = MultipleChoice.objects.get(id=question_id)
                quiz.questions.add(question)
            except ObjectDoesNotExist:
                try:
                    question = PermutationMultipleChoice.objects.get(id=question_id)
                    quiz.questions.add(question)
                except ObjectDoesNotExist:
                    try:
                        question = ParsonsProblem.objects.get(id=question_id)
                        quiz.questions.add(question)
                    except ObjectDoesNotExist:
                        pass
        quiz.save()
        return redirect('quiz_list')
    else:
        questions = {
            'multiple_choice': MultipleChoice.objects.all(),
            'permutation_multiple_choice': PermutationMultipleChoice.objects.all(),
            'parsons_problem': ParsonsProblem.objects.all(),
        }
        selected_questions = quiz.questions.all()
        return render(request, 'update_quiz.html', {'quiz': quiz, 'questions': questions, 'selected_questions': selected_questions})

@login_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        # process the quiz submission
        pass
    else:
        questions = quiz.questions.all()
        context = {
        'quiz': quiz,
        'questions': questions,
        }
    return render(request, 'take_quiz.html', context)