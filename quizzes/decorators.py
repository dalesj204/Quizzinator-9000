from django.shortcuts import redirect
from quizzes.views import *

def user_is_teacher(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_teacher:
                return function(request, *args, **kwargs)
            return render(request, 'permission_error.html')
        else:
            return render(request, 'permission_error.html')
    return wrapper


def user_is_student(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_student:
                return function(request, *args, **kwargs)
            return render(request, 'permission_error.html')
        else:
            return render(request, 'permission_error.html')
    return wrapper