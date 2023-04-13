
from django.test import TestCase
from django.urls import reverse
from .models import Class, Grade, Quiz,Tag, Question, Options, Answer
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

# Create the 'Option' Test
# Author - Shawn Cai
class OptionModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('UnitTest is Testing: ', 'blue')+colored('Option', 'red'))
        super().setUpClass()

    def setUp(self):
        self.question = Question.objects.create(stem="What is the capital of France?", type=0, explain="The capital of France is Paris.")
        self.option1 = Options.objects.create(options=1, content="Paris", question=self.question)
        self.option2 = Options.objects.create(options=2, content="London", question=self.question)

    
    def test_options_content(self):
        self.assertEqual(self.option1.content, "Paris")
        self.assertEqual(self.option2.content, "London")

    def test_options_question(self):
        self.assertEqual(self.option1.question, self.question)
        self.assertEqual(self.option2.question, self.question)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: Option is Tested!', 'green'))

# Create the 'Answer' Test
# Author - Shawn Cai
class AnswerModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('UnitTest is Testing: ', 'blue')+colored('Answer', 'red'))
        super().setUpClass()

    def setUp(self):
        self.question = Question.objects.create(stem="What is the capital of France?", type=0, explain="The capital of France is Paris.")
        self.option1 = Options.objects.create(options=1, content="Paris", question=self.question)
        self.option2 = Options.objects.create(options=2, content="London", question=self.question)
        self.answer = Answer.objects.create(options=1, question=self.question)

    
    def test_correct_answer(self):
        correct_option = Options.objects.get(pk=self.answer.options)
        self.assertEqual(correct_option.content, "Paris")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: Answer is Tested!', 'green'))

# Create the 'Question' Test
# Author - Shawn Cai
class QuestionModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('UnitTest is Testing: ', 'blue')+colored('Question', 'red'))
        super().setUpClass()

    def setUp(self):
        self.question = Question.objects.create(stem="What is the capital of France?", type=0, explain="The capital of France is Paris.")
        self.option1 = Options.objects.create(options=1, content="Paris", question=self.question)
        self.option2 = Options.objects.create(options=2, content="London", question=self.question)
        self.answer = Answer.objects.create(options=1, question=self.question)
        self.tag1 = Tag.objects.create(tag='Geography')
        self.tag2 = Tag.objects.create(tag='Europe')
        self.question.tag.add(self.tag1)
        self.question.tag.add(self.tag2)
    
    def test_question_contains_options(self):
        options = self.question.options_set.all()
        self.assertEqual(len(options), 2)

    def test_question_contains_answer(self):
        answer = self.question.answer_set.first()
        self.assertEqual(answer.options, 1)

    def test_question_contains_tags(self):
        tags = self.question.tag.all()
        self.assertEqual(len(tags), 2)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: Question is Tested!', 'green'))
        
# Create the 'Quiz' Test
# Author - Shawn Cai
class QuizModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('UnitTest is Testing: ', 'blue')+colored('Quiz', 'red'))
        super().setUpClass()

    def setUp(self):
        self.question1 = Question.objects.create(stem="What is the capital of France?", type=0, explain="The capital of France is Paris.")
        self.option1 = Options.objects.create(options=1, content="Paris", question=self.question1)
        self.option2 = Options.objects.create(options=2, content="London", question=self.question1)
        self.answer1 = Answer.objects.create(options=1, question=self.question1)
        self.tag1 = Tag.objects.create(tag='Geography')
        self.tag2 = Tag.objects.create(tag='Europe')
        self.question1.tag.add(self.tag1)
        self.question1.tag.add(self.tag2)

        self.question2 = Question.objects.create(stem="What is the currency of Japan?", type=0, explain="The currency of Japan is the yen.")
        self.option3 = Options.objects.create(options=1, content="Yen", question=self.question2)
        self.option4 = Options.objects.create(options=2, content="Dollar", question=self.question2)
        self.answer2 = Answer.objects.create(options=1, question=self.question2)
        self.tag3 = Tag.objects.create(tag='Economy')
        self.tag4 = Tag.objects.create(tag='Asia')
        self.question2.tag.add(self.tag3)
        self.question2.tag.add(self.tag4)

        start_time = timezone.make_aware(dt(2023, 3, 22, 9, 0, 0))
        end_time = start_time + timedelta(hours=1)
        time_limit = timedelta(minutes=30)

        self.quiz = Quiz.objects.create(name="Geography and Economy Quiz", start_time=start_time, end_time=end_time, time_limit=time_limit)
        self.quiz.questions.add(self.question1)
        self.quiz.questions.add(self.question2)
    
    def test_quiz_contains_questions(self):
        questions = self.quiz.questions.all()
        self.assertEqual(len(questions), 2)

    def test_question_contains_tags_and_answers(self):
        for question in self.quiz.questions.all():
            tags = question.tag.all()
            answer = question.answer_set.first()
            if question == self.question1:
                self.assertEqual(len(tags), 2)
                self.assertEqual(answer.options, 1)
            elif question == self.question2:
                self.assertEqual(len(tags), 2)
                self.assertEqual(answer.options, 1)

    def test_quiz_attributes(self):
        start_time = timezone.make_aware(dt(2023, 3, 22, 9, 0, 0))
        end_time = start_time + timedelta(hours=1)
        time_limit = timedelta(minutes=30)

        self.assertEqual(self.quiz.name, "Geography and Economy Quiz")
        self.assertEqual(self.quiz.start_time, start_time)
        self.assertEqual(self.quiz.end_time, end_time)
        self.assertEqual(self.quiz.time_limit, time_limit)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: Quiz is Tested!', 'green'))

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