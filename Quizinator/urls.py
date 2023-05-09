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
    path('quiz_home/', include('quizzes.urls'), name='index'),
    path('', RedirectView.as_view(url='/login/', permanent=True)),
    path('admin/', admin.site.urls),
    path('admin_toggle/<str:view_id>', views.AdminViewToggle, name='adminViewChange'),
    path('quiz_home/admin_password_reset/', views.AdminPasswordReset, name='adminPasswordReset'),
    
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    # path('register/', views.RegistrationView, name='registration'),
    path('password_reset/', views.ChangePasswordView, name='resetPassword'),
    path('register/student/', views.StudentSignUpView, name='studentRegistration'),
    path('register/teacher/', views.TeacherSignUpView, name='teacherRegistration'),
    
    path('class_detail/<int:class_id>', views.ClassDetailView, name='class_detail'), 
    
    path('quizzes/take/<int:quiz_id>', views.TakeQuizView, name='take_quiz'),
    path('quizzes/take/summary/<int:quiz_id>', views.SubmitQuiz, name='submitQuiz'),
    path('quizzes/gradebook/<int:quiz_id>', views.TeacherGradebookView, name='gradebook'),
    
    path('quiz_create/', user_is_teacher(QuizCreateView.as_view()), name='quiz_create'),
    path('questions/search/', search_questions, name='search_questions'),
    path('quiz_list/', user_is_teacher(QuizListView.as_view()), name='quiz_list'),
    path('quizzes/<int:quiz_id>/summary/', user_is_teacher(QuizSummaryView.as_view()), name='quiz_summary'),
    
    path('questions/', user_is_teacher(views.questionPageView.as_view()), name = 'questionPage'),
    path('export_xcl/', views.export_xcl, name = 'export_xcl'), 
    path('questions/importing/', views.importing, name = 'importing'),
    path('questions/importing/import_xcl/', views.import_xcl, name='importxcl'),
    path('questions/delete/<int:id>', views.delete, name='delete'), # needs confirmation page
    path('questions/add/', views.add, name='add'), # needs error handling and maybe some drop down menus
    path('questions/add/addrecord/', views.addrecord, name='addrecord'),
    path('questions/edit_question/<int:id>', views.edit, name='edit'),
    
    path('addStudent/<int:id>', views.studentPageView, name='addStudent'),
    path('addStudent/addStudentrecord/<int:id>', views.addStudentrecord, name='addStudentrecord'),
    path('addStudent/deleteStudentrecord/<int:id>', views.deleteStudentrecord, name='deleteStudentrecord'),
    
    path('class_detail/stats', views.ClassStatsView.as_view(), name='stats'), # page does not exist yet
]