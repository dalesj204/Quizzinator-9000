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
    path('quiz_list/', views.QuizListView.as_view(), name ='quiz-list'),
    path('quiz/<int:pk>', views.QuizDetailView.as_view(), name='quiz-detail'),
    re_path('studentLogin/',views.studentLogin,name='studentLogin'),
    path('profile/', views.studentProfile,name= 'studentProfile'),
    path('class_list/', views.ClassListView.as_view(), name='classes'),
    path('class_list/<int:class_id>', views.ClassDetailView, name='class_detail'),
    path('class_list/<int:pk>/gradebook', views.ClassGradebookView.as_view(), name='grade_list'),
    path('class_list/stats', views.ClassStatsView.as_view(), name='stats'),
    path('teacher_profile/<int:teacher_id>', views.TeacherHomeView, name='teacher'),
    path('student_profile/<int:student_id>', views.StudentHomeView, name='student'),
]
