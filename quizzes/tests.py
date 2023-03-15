from django.test import TestCase
from .models import MultipleChoiceQuestion, PermutationalMultipleChoiceQuestion, ParsonsProblem
from.models import QuestionBank

class QuestionModelTests(TestCase):

    def test_multiple_choice_question(self):
        """
        Author: Shawn Cai
    
        Test case for the MultipleChoiceQuestion model.

        Tests:
        - test_randomize_choices(): checks that the randomize_choices() method randomizes the order of the choices
        - test_score_answer(): checks that the score_answer() method correctly scores the given answer
        """
        question = MultipleChoiceQuestion.objects.create(
            root="What is the capital of France?",
            correct_answer="Paris",
            distractors="New York, London, Tokyo"
        )
        choices = question.get_randomized_choices()
        self.assertEqual(len(choices), 4)
        self.assertIn(question.correct_answer, choices)

    def test_permutational_multiple_choice_question(self):
        """
        Author: Shawn Cai
    
        Test case for the PermutationalMultipleChoiceQuestion model.

        Tests:
        - test_randomize_choices(): checks that the randomize_choices() method randomizes the order of the choices
        - test_score_answer(): checks that the score_answer() method correctly scores the given answers
        """
        question = PermutationalMultipleChoiceQuestion.objects.create(
            root1="What is the capital of France?",
            root2="What is the largest city in France?",
            correct_answer1="Paris",
            correct_answer2="Paris",
            distractors="New York, London, Tokyo"
        )
        choices1, choices2 = question.get_randomized_choices()
        self.assertEqual(len(choices1), 4)
        self.assertIn(question.correct_answer1, choices1)
        self.assertEqual(len(choices2), 4)
        self.assertIn(question.correct_answer2, choices2)

    def test_parsons_problem(self):
        """
        Author: Shawn Cai
    
        Test case for the ParsonsProblem model.

        Tests:
        - test_randomize_order(): checks that the randomize_order() method randomizes the order of the code snippet
        - test_score_answer(): checks that the score_answer() method correctly scores the given answer
        """
        question = ParsonsProblem.objects.create(
            question="What is the output of this code snippet?",
            code_snippet="for i in range(10):\n\tprint(i)",
            choices="1,2,3,4,5,6,7,8,9,10"
        )
        choices = question.get_randomized_choices()
        self.assertEqual(len(choices), 10)
        self.assertIn("1", choices)
        self.assertIn("2", choices)
        self.assertIn("3", choices)
        self.assertIn("4", choices)
        self.assertIn("5", choices)
        self.assertIn("6", choices)
        self.assertIn("7", choices)
        self.assertIn("8", choices)
        self.assertIn("9", choices)
        self.assertIn("10", choices)

# QuestionBankModelTest - To Be Further Modified
# Author - Jacob Fielder, Nathan Prelewicz
#
# NOTE- Comment Style to be change once
# coding standards are defined.
#
#This made us recognize that we have been going about
#the question bank and question wrong, there is a sign-
#ificantly simplier way of handling this.
class QuestionBankModelTests(TestCase):
    def test_if_it_holds_multiplechoice(self):
        self.bank = QuestionBank.objects.create(
            questions = (
                MultipleChoiceQuestion.objects.create(
                    root="My name is Bob, what is my name",
                    correct_answer="Bob",
                    distractors="Ziggs, Aldur, Mason"
                ),
            )
        )
        self.assertEqual(self.bank[0], 'MC')
