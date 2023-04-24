
from django.test import TestCase
from django.urls import reverse
from .models import Class, Grade, Quiz,Tag, Question, Options
from datetime import datetime as dt, timedelta
from django.utils import timezone
from termcolor import colored

# Create the 'Tag' Test
# Author - Shawn Cai
class TagTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('UnitTest is Testing: ', 'blue')+colored('Tag', 'red'))
        super().setUpClass()

    def setUp(self):
        self.question = Question.objects.create(stem="What is the capital of France?", type=0, explain="The capital of France is Paris.")
        self.tag1 = Tag.objects.create(tag='Geography')
        self.tag2 = Tag.objects.create(tag='Europe')
    
    def test_question_type(self):
        self.assertEqual(self.question.type, 0)

    def test_question_explain(self):
        self.assertEqual(self.question.explain, "The capital of France is Paris.")

    def test_question_tag(self):
        self.question.tag.add(self.tag1)
        self.question.tag.add(self.tag2)
        self.assertEqual(self.question.tag.count(), 2)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: Tag is Tested!', 'green'))

# Create the 'Class' Test
# Author - Shawn Cai
class TestClassModel(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('UnitTest is Testing: ', 'blue')+colored('Class', 'red'))
        super().setUpClass()
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        classer = Class(name = "Assembly", gradebook = Grade.objects.create(name = "quiz one", grade = 55))
        classer.save()
        # quizzer = classer.quizzes.create(name = "Quiz One", course = "Assembly", startDate = "2023-03-23", endDate = "2023-04-24")
        # quizzer.save()

        
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

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: Classes is Tested!', 'green'))
    
    # def test_quizzer(self):
    #     pracClass = Class.objects.create(name = "Assembly", gradebook = Grade.objects.create(name = "quiz one", grade = 55))
    #     pracQuizOne = Quiz.objects.create(name = "Quiz One", course = "Assembly", startDate = "2023-03-23", endDate = "2023-04-24")
    #     pracQuizTwo = Quiz.objects.create(name = "Quiz Two", course = "Assembly", startDate = "2023-03-16", endDate = "2023-04-17")
    #     pracClass.quizzes.set([pracQuizOne.pk, pracQuizTwo.pk])
    #     self.assertEqual(pracQuizOne.name, "Quiz One")
    #     self.assertEqual(pracQuizTwo.name, "Quiz Two")
    #     self.assertEqual(pracQuizOne.course, "Assembly")
    #     self.assertEqual(pracQuizTwo.course, "Assembly")
    #     self.assertEqual(pracQuizOne.startDate, "2023-03-23")
    #     self.assertEqual(pracQuizTwo.startDate, "2023-03-16")
    #     self.assertEqual(pracQuizOne.endDate, "2023-04-24")
    #     self.assertEqual(pracQuizTwo.endDate, "2023-04-17")
    #     self.assertEqual(pracClass.quizzes.count(), 2)

    def test_class_gradebook(self):
        pracClass = Class.objects.create(name = "Assembly", gradebook = Grade.objects.create(name = "quiz one", grade = 55))
        self.assertEqual(pracClass.gradebook.name, "quiz one")
        self.assertEqual(pracClass.gradebook.grade, 55)