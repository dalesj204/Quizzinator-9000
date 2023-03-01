
from django.test import TestCase
from django.db import models
from django.urls import reverse
from quiz_home.models import Class, Grade, Quiz

class ClassModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        classer = Class(name = "Assembly", gradebook = Grade.objects.create(name = "quiz one", grade = 55))
        classer.save()
        quizzer = classer.quizzes.create(name = "Quiz One", course = "Assembly", startDate = "2023-03-23", endDate = "2023-04-24")
        quizzer.save()
    
    def test_name_label(self):
        className = Class.objects.get(id=1)
        field_label = className._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_quizzes_label(self):
        className = Class.objects.get(id=1)
        field_label = className._meta.get_field('quizzes').verbose_name
        self.assertEqual(field_label, 'quizzes')

    def test_gradebook_label(self):
        className = Class.objects.get(id=1)
        field_label = className._meta.get_field('gradebook').verbose_name
        self.assertEqual(field_label, 'gradebook')

    def test_name_max_length(self):
        className = Class.objects.get(id=1)
        max_length = className._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_name(self):
        className = Class.objects.get(id=1)
        expected_object_name = className.name
        self.assertEqual(str(className), expected_object_name)
          
    def test_get_absolute_url(self):
        className = Class.objects.get(id=1)
        self.assertEqual(className.get_absolute_url(), '/class_list/1')
    
    def test_quizzer(self):
        pracClass = Class.objects.create(name = "Assembly", gradebook = Grade.objects.create(name = "quiz one", grade = 55))
        pracQuizOne = Quiz.objects.create(name = "Quiz One", course = "Assembly", startDate = "2023-03-23", endDate = "2023-04-24")
        pracQuizTwo = Quiz.objects.create(name = "Quiz Two", course = "Assembly", startDate = "2023-03-16", endDate = "2023-04-17")
        pracClass.quizzes.set([pracQuizOne.pk, pracQuizTwo.pk])
        self.assertEqual(pracQuizOne.name, "Quiz One")
        self.assertEqual(pracQuizTwo.name, "Quiz Two")
        self.assertEqual(pracQuizOne.course, "Assembly")
        self.assertEqual(pracQuizTwo.course, "Assembly")
        self.assertEqual(pracQuizOne.startDate, "2023-03-23")
        self.assertEqual(pracQuizTwo.startDate, "2023-03-16")
        self.assertEqual(pracQuizOne.endDate, "2023-04-24")
        self.assertEqual(pracQuizTwo.endDate, "2023-04-17")
        self.assertEqual(pracClass.quizzes.count(), 2)

    def test_class_gradebook(self):
        pracClass = Class.objects.create(name = "Assembly", gradebook = Grade.objects.create(name = "quiz one", grade = 55))
        self.assertEqual(pracClass.gradebook.name, "quiz one")
        self.assertEqual(pracClass.gradebook.grade, 55)