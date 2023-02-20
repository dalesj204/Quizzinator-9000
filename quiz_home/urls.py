from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quizzes/', views.QuizListView.as_view(), name ='quizzes')
]
