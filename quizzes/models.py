import random
from django.db import models

class MultipleChoiceQuestion(models.Model):
    """
    Author: Shawn Cai
    
    A model for a standard multiple choice question.

    Fields:
    - root (CharField): the root of the question
    - correct_answer (CharField): the correct answer
    - distractors (ArrayField): an array of plausible distractors

    Methods:
    - randomize_choices(): randomizes the order of the choices
    - score_answer(answer: str) -> float: scores the given answer
    """
    root = models.TextField()
    correct_answer = models.TextField()
    distractors = models.TextField()
    hint = models.TextField(blank=True, null=True)

    def get_randomized_choices(self):
        choices = [self.correct_answer] + self.distractors.split(",")
        random.shuffle(choices)
        return choices
    

class PermutationalMultipleChoiceQuestion(models.Model):
    """
    Author: Shawn Cai

    A model for a permutational multiple choice question.

    Fields:
    - root_1 (CharField): the first root of the question
    - correct_answer_1 (CharField): the correct answer for the first root
    - root_2 (CharField): the second root of the question
    - correct_answer_2 (CharField): the correct answer for the second root
    - distractors (ArrayField): an array of plausible distractors

    Methods:
    - randomize_choices(): randomizes the order of the choices
    - score_answer(answer_1: str, answer_2: str) -> float: scores the given answers
    """
    root1 = models.TextField()
    root2 = models.TextField()
    correct_answer1 = models.TextField()
    correct_answer2 = models.TextField()
    distractors = models.TextField()
    hint = models.TextField(blank=True, null=True)

    def get_randomized_choices(self):
        choices1 = [self.correct_answer1] + self.distractors.split(",")
        random.shuffle(choices1)
        choices2 = [self.correct_answer2] + self.distractors.split(",")
        random.shuffle(choices2)
        return choices1, choices2


class ParsonsProblem(models.Model):
    """
    Author: Shawn Cai

    A model for a Parson's problem.

    Fields:
    - question (CharField): the question to be answered
    - code_snippet (TextField): the code snippet to be put in order

    Methods:
    - randomize_order(): randomizes the order of the code snippet
    - score_answer(answer: List[int]) -> float: scores the given answer
    """
    question = models.TextField()
    code_snippet = models.TextField()
    choices = models.TextField()
    hint = models.TextField(blank=True, null=True)

    def get_randomized_choices(self):
        choices = self.choices.split(",")
        random.shuffle(choices)
        return choices
    

# QuestionBank Model - To Be Further Modified
# Author - Jacob Fielder
#
# NOTE- Comment Style to be change once
# coding standards are defined.
#
#The Question Bank model is simplistic in its inital design
#due to multiple choice questions being the only type curr-
#ently completed. As more questions types are developed, this
#will grow in complexity.
class QuestionBank(models.Model):
    #Tags for the tags for specific questions in our bank.
    QUESTION_TYPE = (
      ('MC', 'Multiple Choice'),
      ('PP', 'Parsens Problem'),
      ('PMC', 'Permutation Problem'),
    )

    #Have the bank point towards the question type models.
    questions = (
        ('MC',models.ForeignKey(MultipleChoiceQuestion,
                on_delete=models.CASCADE)),
        ('PMC',models.ForeignKey(PermutationalMultipleChoiceQuestion,
                on_delete=models.CASCADE)),
        ('PP',models.ForeignKey(ParsonsProblem,
                on_delete=models.CASCADE))
    )