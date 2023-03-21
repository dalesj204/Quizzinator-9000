"""Quizinator URL Configuration

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
# from django.conf.urls import url
from quiz_home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/quiz_home/', permanent=True)),
    path('quiz_home/', include('quiz_home.urls')),
    re_path('studentLogin/',views.studentLogin,name='studentLogin'),
    path('profile/<int:pk>', views.studentProfile,name= 'studentProfile2'),
     path('profile/', views.studentProfile,name= 'studentProfile'),
    path('class_list/', views.ClassListView.as_view(), name='classes'),
    path('class_list/<int:class_id>', views.ClassDetailView, name='class_detail'),
    path('class_list/<int:class_id>/gradebook', views.ClassGradebookView.as_view(), name='grade_list'),
    path('class_list/stats', views.ClassStatsView.as_view(), name='stats'),
    path('teacher_profile/<int:teacher_id>', views.TeacherHomeView, name='teacher'),
    path('student_profile/<int:student_id>', views.StudentHomeView, name='student'),
    path('questions/', views.questionPageView.as_view(), name = 'questionPage'),
    path('export_xcl/', views.export_xcl, name = 'export_xcl'),
    path('register/student', views.StudentSignUpView.as_view(), name='studentRegistration'),
    path('register/teacher', views.TeacherSignUpView.as_view(), name='teacherRegistration'),
    path('questions/importing/', views.importing, name = 'importing'),
    path('questions/importing/import_xcl/', views.import_xcl, name='importxcl'),
    # path('questions/delete/<int:id>', views.delete, name='delete'),
    path('questions/add/', views.add, name='add'),
    path('questions/add/addrecord/', views.addrecord, name='addrecord'),
]
from quizzes.views import *
 
urlpatterns += [
    path('Question/index/', QuestionView.as_view(), name='test_qs'),
    path('Question/add/', QuestionAddView.as_view(), name='add_qs'),
    path('Question/update/', QuestionUpdateView.as_view(), name='update_qs'),
    path('Question/delete/', QuestionDeleteView.as_view(), name='delete_qs'),
]