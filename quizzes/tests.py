from django.test import TestCase
from .models import Tag, Question, Options, Answer, Quiz
from datetime import datetime as dt, timedelta
from django.utils import timezone

# Create the 'Tag' Test
# Author - Shawn Cai
class TagTestCase(TestCase):
    def setUp(self):
        self.question = Question.objects.create(stem="What is the capital of France?", type=0, explain="The capital of France is Paris.")
        self.tag1 = Tag.objects.create(tag='Geography')
        self.tag2 = Tag.objects.create(tag='Europe')
    @classmethod
    def setUpClass(cls):
        print("Tag is Testing")
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("Tag Tested!")
    
    def test_question_type(self):
        self.assertEqual(self.question.type, 0)

    def test_question_explain(self):
        self.assertEqual(self.question.explain, "The capital of France is Paris.")

    def test_question_tag(self):
        self.question.tag.add(self.tag1)
        self.question.tag.add(self.tag2)
        self.assertEqual(self.question.tag.count(), 2)

# Create the 'Option' Test
# Author - Shawn Cai
class OptionsModelTest(TestCase):
    def setUp(self):
        self.question = Question.objects.create(stem="What is the capital of France?", type=0, explain="The capital of France is Paris.")
        self.option1 = Options.objects.create(options=1, content="Paris", question=self.question)
        self.option2 = Options.objects.create(options=2, content="London", question=self.question)

    @classmethod
    def setUpClass(cls):
        print("Option is Testing")
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("Option Tested!")
    
    def test_options_content(self):
        self.assertEqual(self.option1.content, "Paris")
        self.assertEqual(self.option2.content, "London")

    def test_options_question(self):
        self.assertEqual(self.option1.question, self.question)
        self.assertEqual(self.option2.question, self.question)

# Create the 'Answer' Test
# Author - Shawn Cai
class AnswerModelTest(TestCase):
    def setUp(self):
        self.question = Question.objects.create(stem="What is the capital of France?", type=0, explain="The capital of France is Paris.")
        self.option1 = Options.objects.create(options=1, content="Paris", question=self.question)
        self.option2 = Options.objects.create(options=2, content="London", question=self.question)
        self.answer = Answer.objects.create(options=1, question=self.question)

    @classmethod
    def setUpClass(cls):
        print("Answer is Testing")
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("Answer Tested!")
    
    def test_correct_answer(self):
        correct_option = Options.objects.get(pk=self.answer.options)
        self.assertEqual(correct_option.content, "Paris")

# Create the 'Question' Test
# Author - Shawn Cai
class QuestionModelTest(TestCase):
    def setUp(self):
        self.question = Question.objects.create(stem="What is the capital of France?", type=0, explain="The capital of France is Paris.")
        self.option1 = Options.objects.create(options=1, content="Paris", question=self.question)
        self.option2 = Options.objects.create(options=2, content="London", question=self.question)
        self.answer = Answer.objects.create(options=1, question=self.question)
        self.tag1 = Tag.objects.create(tag='Geography')
        self.tag2 = Tag.objects.create(tag='Europe')
        self.question.tag.add(self.tag1)
        self.question.tag.add(self.tag2)

    @classmethod
    def setUpClass(cls):
        print("Question is Testing")
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("Question Tested!")
    
    def test_question_contains_options(self):
        options = self.question.options_set.all()
        self.assertEqual(len(options), 2)

    def test_question_contains_answer(self):
        answer = self.question.answer_set.first()
        self.assertEqual(answer.options, 1)

    def test_question_contains_tags(self):
        tags = self.question.tag.all()
        self.assertEqual(len(tags), 2)

# Create the 'Quiz' Test
# Author - Shawn Cai
class QuizModelTest(TestCase):
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

    @classmethod
    def setUpClass(cls):
        print("Quiz is Testing")
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("Quiz Tested!")
    
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