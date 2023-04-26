"""
Quizinator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.urls import include
from quizzes.views import *

urlpatterns = [
    path('quizzes/<int:quiz_id>/summary/', QuizSummaryView.as_view(), name='quiz_summary'),
    path('quizzes/take/<int:quiz_id>', views.TakeQuizView, name='take_quiz'),
    path('quizzes/take/summary/<int:quiz_id>', views.SubmitQuiz, name='submitQuiz'),
    path('quiz_create/', QuizCreateView.as_view(), name='quiz_create'),
    path('quiz_list/', QuizListView.as_view(), name='quiz_list'),
    path('questions/search/', search_questions, name='search_questions'),
    path('admin/', admin.site.urls),
    path('quiz_home/', include('quizzes.urls')),
    path('', RedirectView.as_view(url='/quiz_home/', permanent=True)),
    path('class_list/', views.ClassListView.as_view(), name='classes'),
    path('class_list/<int:class_id>', views.ClassDetailView, name='class_detail'),
    path('class_list/<int:class_id>/gradebook', views.ClassGradebookView.as_view(), name='grade_list'),
    path('class_list/stats', views.ClassStatsView.as_view(), name='stats'),
    path('questions/', views.questionPageView.as_view(), name = 'questionPage'),
    path('export_xcl/', views.export_xcl, name = 'export_xcl'),
    path('questions/importing/', views.importing, name = 'importing'),
    path('questions/importing/import_xcl/', views.import_xcl, name='importxcl'),
    path('questions/delete/<int:id>', views.delete, name='delete'),
    path('questions/add/', views.add, name='add'),
    path('questions/add/addrecord/', views.addrecord, name='addrecord'),
    path('addStudent/<int:id>', views.studentPageView, name='addStudent'),
    path('addStudent/addStudentrecord/<int:id>', views.addStudentrecord, name='addStudentrecord'),
    path('addStudent/deleteStudentrecord/<int:id>', views.deleteStudentrecord, name='deleteStudentrecord'),
    path('questions/edit_question/<int:id>', views.edit, name='edit'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('register/', views.RegistrationView, name='registration'),
    path('register/student', views.StudentSignUpView, name='studentRegistration'),
    path('register/teacher', views.TeacherSignUpView, name='teacherRegistration'),
    path('teacher_profile/', views.TeacherHomeView, name='teacher'),
    path('student_profile/', views.StudentHomeView, name='student'),
]