
from django.test import TestCase
from django.urls import reverse
from .models import Class, Grade, Quiz, Tag, Question, Options
from datetime import datetime as dt, timedelta
from django.utils import timezone
from termcolor import colored

# Create the 'Tag' Test
# Author - Shawn Cai
# Revised - Hayden Dustin - 4/46/23
class TagTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('UnitTest is Testing: ', 'blue')+colored('Tag', 'red'))
        super().setUpClass()

    def setUp(self):
        self.opt = Options(content="temp")
        self.opt.save()
        self.opt2 = Options(content = "temp2")
        self.opt2.save()

        self.question = Question(
            stem="What is the capital of France?",
            type=0,
            explain="The capital of France is Paris.",
            correctOption = self.opt
            )
        self.question.save()
        self.question.options.set([self.opt, self.opt2])

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
        self.assertEqual(className.get_absolute_url(), '/class_detail/1')

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


class QuizModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('Quiz Model is Testing: ', 'blue'))
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n The Quiz Model is Tested!', 'green'))
    @classmethod
    def setUpTestData(self):
        # ###QUESTION 1 SETUP###
        # Options
        opt1_ques1 = Options.objects.create(content = "Computer Part University")
        opt1_ques1.save()
        opt2_ques1 = Options.objects.create(content = "Central Processing Unit")
        opt2_ques1.save()
        opt3_ques1 = Options.objects.create(content = "Computer Processing Unit")
        opt3_ques1.save()

        # Tags
        tag1_ques1 = Tag.objects.create(tag = "Hardware")
        tag1_ques1.save()

        # Question
        ques1 = Question.objects.create(
            stem = "What is a CPU?",
            type = 0,
            explain = "It has nothing to do with University",
            tag = tag1_ques1,
            options = [opt1_ques1, opt2_ques1, opt3_ques1],
            correctOption = opt2_ques1
            )
        ques1.save()
        
        ###QUESTION 2 SETUP###
        # Options
        opt1_ques2 = Options.objects.create(content = "Turring Machine")
        opt1_ques2.save()
        opt2_ques2 = Options.objects.create(content = "Turbine Machine")
        opt2_ques2.save()
        opt3_ques2 = Options.objects.create(content = "Macbook Home")
        opt3_ques2.save()

        # Tags
        tag1_ques2 = Tag.objects.create(tag = "History")
        tag1_ques2.save()

        # Question
        ques2 = Question.objects.create(
            stem = "What was the first computer called?",
            type = 0,
            explain = "It had machine in its name",
            tag = tag1_ques2,
            options = [opt1_ques2, opt2_ques2, opt3_ques2],
            correctOption = opt1_ques2
            )
        ques2.save()
        
        ###QUESTION 3 SETUP###
        # Options
        opt1_ques3 = Options.objects.create(content = "Chicken")
        opt1_ques3.save()
        opt2_ques3 = Options.objects.create(content = "Egg")
        opt2_ques3.save()
        opt3_ques3 = Options.objects.create(content = "Who cares?")
        opt3_ques3.save()

        # Tags
        tag1_ques3 = Tag.objects.create(tag = "Impossible")
        tag1_ques3.save()

        # Question
        ques3 = Question.objects.create(
            stem = "What came first?",
            type = 0,
            explain = "This question is definitely asked WAY too much",
            tag = tag1_ques3,
            options = [opt1_ques3, opt2_ques3, opt3_ques3],
            correctOption = opt3_ques3
            )
        ques3.save()
        
        # Quiz Setup
        quiz = Quiz.objects.create(name = "Example Quiz", questions = [ques1, ques2, ques3], start_time = timezone.now, end_time = timezone.now, pasingThreshold = 70)
        quiz.save()

        questions = list(quiz.questions.all())
        self.assertEqual(questions[1], opt2_ques1)
        self.assertEqual(questions[2], opt1_ques2)
        self.assertEqual(questions[3], opt3_ques3)