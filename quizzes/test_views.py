from django.test import TestCase, Client
from django.urls import reverse
from quizzes.forms import questionForm
from .models import Quiz, Question, Tag, Option, Type, User, Student, Options, Answer, Class, Grade
import xlrd
from termcolor import colored   
import os, xlwt, tablib
from xlwt import Workbook
import openpyxl
from django.core.files.uploadedfile import SimpleUploadedFile
import json
from django.utils import timezone

class studentInClassTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('Students in Class is Testing: ', 'blue'))
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: Students in Class is Tested!', 'green'))
    @classmethod
    def setUpTestData(self):
        User.objects.create(id = '111111111111',is_student = True, is_teacher = False,first_name = 'Jasmine', last_name = 'James', email = 'jj@me.com')
        studentOneUser = User.objects.get(id = '111111111111')
        studentOneUser.set_password("SlappedHam123")
        studentOneUser.save()
        # User.objects.create(id = '111111111112',is_student = True, is_teacher = False,first_name = 'Belle', last_name = 'Brown', email = 'BelleBrown@me.com')
        # studentTwoUser = User.objects.get(id = '111111111112')
        # studentTwoUser.set_password("SlappedHam1234")
        # studentTwoUser.save()
        # User.objects.create(id = '111111111113',is_student = True, is_teacher = False,first_name = 'Snow', last_name = 'Smith', email = 'SS@me.com')
        # studentThreeUser = User.objects.get(id = '111111111113')
        # studentThreeUser.set_password("SlappedHam1235")
        classer = Class(name = "CIS201", gradebook = Grade.objects.create(name = "quiz one", grade = 55))
        classer.save()
        studentOne = Student.objects.create(user = studentOneUser)
        studentOne.classes.add(classer)
        studentOne.save()
        # studentTwo = Student.objects.create(user = studentTwoUser,classes = classOne)
        # studentTwo.save()

    def test_num_students_class(self):
        self.assertEqual(len(Student.objects.all().filter(classes=1)), 1)
    
    # def test_remove_student_class(self):
    #     data = {'selectedStudent2': ['1']}
    #     response = self.client.post('addStudent/deleteStudentrecord/1', data)
    #     self.assertEqual(response.status_code, 200)
class questionListViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('QuestionList is Testing: ', 'blue'))
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: QuestionList is Tested!', 'green'))

    @classmethod
    def setUpTestData(self):
        
        # Create 3 questions
        number_of_questions = 3
        count = 1
        for question_id in range(number_of_questions):
            ques =Question.objects.create(
                stem=f'What is one plus one?',
                type=0,
                explain=f'It is odd',
            )
            ques.save()
            tag1 = Tag.objects.create(tag =f'CIS201')
            tag2 = Tag.objects.create(tag =f'CIS202')
            ques.tag.add(tag1, tag2)
            ques.save()
            q = Question.objects.get(id = count)
            op = Options.objects.create(
                content = "fake answer",
                question = q
            )
            op.save()
            op2 = Options.objects.create(
                content = "real answer",
                question = q
            )
            op2.save()
            ans = Answer.objects.create(
                opt = op2,
                question = q
            )
            ans.save()
            count = count + 1
    
            

    def test_question_page_view_url_exists_at_desired_location(self):
        response = self.client.get('/questions/')
        self.assertEqual(response.status_code, 200)

    def test_question_page_view_url_accessible_by_name(self):
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)

    def test_question_page_view_uses_correct_template(self):
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questionPage.html')


    def test_question_page_lists_all_questions(self):
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['question_list']), 3)

    def test_question_content(self):
        self.assertEqual(Question.objects.get(id = 1).stem, 'What is one plus one?')
        self.assertEqual(Question.objects.get(id = 1).type, 0)
        self.assertEqual(Question.objects.get(id = 1).explain, 'It is odd')
    
    @classmethod
    def setUpClass(cls):
        print(colored('OptionList is Testing: ', 'blue'))
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: OptionList is Tested!', 'green'))
    @classmethod
    def setUpClass(cls):
        print(colored('AnswerList is Testing: ', 'blue'))
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: AnswerList is Tested!', 'green'))
    def test_options_length(self):
        self.assertEqual(len(Options.objects.all()), 6)
    
    def test_Answer_length(self):
        self.assertEqual(len(Answer.objects.all()), 3)
    
    def test_options_content(self):
        self.assertEqual(Options.objects.get(id = 1).content, 'fake answer')
    
    def test_Answer_content(self):
         ans = Answer.objects.get(id = 1).opt
         self.assertEqual(ans.content, 'real answer')
    @classmethod
    def setUpClass(cls):
        print(colored('Delete Question is Testing: ', 'blue'))
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: Delete Question is Tested!', 'green'))
    #Delete a question and test the length and if the id exists to see if it deletes
    def test_delete_button_view_url_accessible_by_name_and_deletion_works(self):
        ques = Question.objects.get(id=1)
        response = self.client.post(reverse('delete', args=(ques.id,)), follow=True)
        self.assertRedirects(response, reverse('questionPage'), status_code = 302)
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['question_list']), 2)
        self.assertFalse(Question.objects.filter(pk=1).exists())
       

class editViewTest(TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     print(colored('Edit Question is Testing: ', 'blue'))
    #     super().setUpClass()
    # @classmethod
    # def tearDownClass(cls):
    #     super().tearDownClass()
    #     print("/"+colored('\n Model: Edit Question is Tested!', 'green'))
    @classmethod
    def setUpTestData(self):
       # Create 1 question
        
        self.question = Question.objects.create(stem="what is two plus two", type=1, explain="two plus two is four.")
        self.question.tag.create(tag='math')
        self.question.save()
            
    # #should not create a new question but alter existing question, so length of question list should stay the same
    # def test_edit_button_view_url_accessible_by_name_and_length_is_same(self):
    #     self.assertEqual(self.question.stem, "what is two plus two")
    #     ques = questionForm(instance = self.question).initial
    #     ques['stem'] ='What is an apple?'
    #     ques['type'] =1
    #     ques['explain'] ='It is a fruit'
    #     #this needs selenium to click the tags
    #     ques['tag']  = 
    #     ques['Update'] = True
        
    #     self.assertEqual(ques['stem'], "What is an apple?")
    #     response = self.client.post(url = 'edit', path = '/questions/edit_question/1',data = ques)
    #     self.assertEqual(response.status_code, 200)
    #     response = self.client.get(reverse('questionPage'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(response.context['question_list']), 1)
    #     self.question.refresh_from_db()
    #     self.assertEqual(self.question.stem, "What is an apple?")
   
class exportTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('Exporting is Testing: ', 'blue'))
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: Exporting is Tested!', 'green'))
    @classmethod
    def setUpTestData(self):

        self.ques =Question.objects.create(
            stem=f'What is one plus one?',
            type=0,
            explain=f'It is odd',
        )
        tag1 = Tag.objects.create(tag =f'CIS201')
        tag2 = Tag.objects.create(tag =f'CIS202')
        self.ques.tag.add(tag1, tag2)
        self.ques =Question.objects.create(
            stem=f'What is one plus one?',
            type=0,
            explain=f'It is odd',
        )
        tag1 = Tag.objects.create(tag =f'CIS201')
        tag2 = Tag.objects.create(tag =f'CIS202')
        self.ques.tag.add(tag1, tag2)
        self.ques =Question.objects.create(
            stem=f'What is one plus one?',
            type=0,
            explain=f'It is odd',
        )
        tag1 = Tag.objects.create(tag =f'CIS201')
        tag2 = Tag.objects.create(tag =f'CIS202')
        self.ques.tag.add(tag1, tag2)

    def test_export_view_url_exists_at_desired_location(self):
        response = self.client.get('/export_xcl/')
        self.assertEqual(response.status_code, 200)

    def test_export_view_url_accessible_by_name(self):
        response = self.client.get(reverse('export_xcl'))
        self.assertEqual(response.status_code, 200)
    def test_export_question_page_lists_all_questions(self):
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['question_list']), 3)

    def test_export(self):
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        data = {'file_format': str("xls")}
        response = self.client.post('/export_xcl/', data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.has_header("Content-Disposition"))
        self.assertEqual(response['Content-Type'],
            'application/ms-excel')
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename=filename.xls'
        )
#         print(response.context)
#         workbook = xlrd.open_workbook(response.content)

#         #Get the first sheet in the workbook by index
#         sheet1 = workbook.sheet_by_index(0)

#         #Get each row in the sheet as a list and print the list
#         for rowNumber in range(sheet1.nrows):
#             row = sheet1.row_values(rowNumber)
#             print(row)


class addPageTest(TestCase):
    @classmethod
    def setUpTestData(self):
        print(colored('View testing: ', 'blue')+colored('Add Page', 'red'))
        # Create 1 question
        
        self.question = Question.objects.create(stem="what is two plus two", type=1, explain="two plus two is four.")
        self.tag1 = Tag.objects.create(tag='math')
        self.tag2 = Tag.objects.create(tag='addition')
            
        
    def test_add_page_view_url_exists_at_desired_location(self):
        # print("Tested Add Page View exists at the correct URL.")
        response = self.client.get('/questions/add/')
        self.assertEqual(response.status_code, 200)

    def test_add_page_view_url_accessible_by_name(self):
        # print("Tested that Add Page URL is accessible by name.")
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)

    def test_add_page_view_uses_correct_template(self):
        # print("Tested that Add Page URL uses the correct template.")
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add.html')  
    
    def test_add_and_submit_button(self):
        # print("Tested the 'Add and Submit' Button.")
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(len(response.context['question_list']), 1)
        response = self.client.post("/questions/add/addrecord/", {'stem':'something', 'type':2, 'explain': 'none', 'tag': 'hi'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['question_list']), 2)
    
    def test_submit_and_add_another_button(self):
        # print("Tested the 'Submit and Add Another' Button.")
        response = self.client.post("/questions/add/addrecord/", {'stem':'something else', 'type':1, 'explain': 'explaination here', 'tag': 'bye'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('add'))
        
        response = self.client.post("/questions/add/addrecord/", {'stem':'another question stem', 'type':0, 'explain': 'explaination2 here', 'tag': 'tag num here'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(len(response.context['question_list']), 3)
              
    # # need help with the cancel button
    # def test_cancel_button(self):
    #     print("Tested the Cancel Button.")
        
    #     response = self.client.get("/questions/add/")
    #     self.assertEqual(response.status_code, 200)
    #     response = self.client.get(reverse('questionPage'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(response.context['question_list']), 1)
    
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n View: Add Page and Buttons are Tested!', 'green'))
class importTest(TestCase):
    @classmethod
    def setUpTestData(self):
        print(colored('View testing: ', 'blue')+colored('Import', 'red'))
        # Create 2 questions
        self.question = Question.objects.create(stem="What is the capital of New York?", type=1, explain="The capital of New York is Albany.")
        self.tag1 = Tag.objects.create(tag='Geography')
        self.tag2 = Tag.objects.create(tag='New York')
        
        self.question2 = Question.objects.create(stem="What color is the sky?", type=2, explain="The sky is blue.")
        self.tag3 = Tag.objects.create(tag='Colors')
        
        

    def test_import_view_url_exists_at_desired_location(self):
        response = self.client.get('/questions/importing/')
        self.assertEqual(response.status_code, 200)

    def test_import_view_url_accessible_by_name(self):
        response = self.client.get(reverse('importing'))
        self.assertEqual(response.status_code, 200)

    def test_add_view_url_exists_at_desired_location(self):
        response = self.client.get('/questions/add/')
        self.assertEqual(response.status_code, 200)

    def test_add_view_url_accessible_by_name(self):
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)
        
    def test_importing_file(self):
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        # response = self.client.get(reverse('importing'))
        # self.assertEqual(response.status_code, 200)
        # response = self.client.get(reverse('importxcl'))
        # self.assertEqual(response.status_code, 200)
        
        # create file to import
        wb = Workbook()
        sheet = wb.add_sheet('Sheet 1')
        sheet.write(0, 0, 'ID')
        sheet.write(0, 1, 'Question')
        sheet.write(0, 2, 'Type')
        sheet.write(0, 3, 'Hint')
        sheet.write(0, 4, 'Tags')
        sheet.write(1, 0, '1')
        sheet.write(1, 1, 'What does // mean?')
        sheet.write(1, 2, 'PP')
        sheet.write(1, 3, 'it is a type of comment')
        sheet.write(1, 4, 'Java|CIS')
        sheet.write(2, 0, '2')
        sheet.write(2, 1, 'What is two times two?')
        sheet.write(2, 2, 'MC')
        sheet.write(2, 3, 'the same as addition')
        sheet.write(2, 4, 'Math|Multiplication')
        wb.save('import_test_file.xls')
        
        # data = SimpleUploadedFile('import_test_file.xls', content_type="xls")
        # response = self.client.post(reverse('importxcl'),content='import_test_file.xls' )
        # self.assertEqual(response.status_code, 200)
        
        # os.remove("import_test_file.xls") # delete file after test is done
        # for row in sheet.iter_rows():
        #     temp = []
        #     for tag in data[4].split('|'):
        #         h = Tag(tag = tag)
        #         h.save()
        #         temp.append(h)
        #     value = Question(
        #         row[0], # ID
        #         row[1], # stem
        #         row[2], # type
        #         row[3], # explain
        #     )
        #     value.save()
        #     value.tag.add(*temp)
        #     value.save()
        # return HttpResponseRedirect(reverse('questionPage'))
    
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n View: Import is Tested!', 'green'))


class LoginTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('Login is Testing: ', 'blue'))
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: Login is Tested!', 'green'))
    @classmethod
    def setUp(self):
        
        User.objects.create(
            id="111222333444",
            is_student=True,
            is_teacher=False,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        Student.objects.create(
            user=this_user
        )
        student = Student.objects.all().first()

    def test_create_user(self):
        this_user = User.objects.all().first()
        student = Student.objects.all().first()
        response = self.client.get(reverse('student'))#, kwargs={'student_id': student.user.id}
        # Redirects to the login page as intended - hence 302 status code
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        this_user = User.objects.all().first()
        student = Student.objects.all().first()
        self.client.login(username="test@test.com", password="SlappedHam123")
        
        response = self.client.get(reverse('student'))#, kwargs={'student_id': student.user.id}
        # No longer redirects because you are logged in as Richie Man
        self.assertEqual(response.status_code, 200)

# QuizCreateViewTest - Tests is the if  QuizCreateView is working.
#
# Author - Jacob Fielder
class QuizCreateViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(colored('\nUnitTest is Testing:', 'blue') + colored(' QuizCreateView', 'red'))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print(colored('View: QuizCreateView is Tested!', 'green'))

    def setUp(self):
        self.client = Client()
        self.url = reverse('quiz_create')
        self.data = {
            'quiz_name': 'Test Quiz',
            'start_time': timezone.localtime().strftime('%Y-%m-%dT%H:%M'),
            'end_time': (timezone.localtime() + timezone.timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M'),
            'stem': 'test',
            'questions': ['test question'],
        }
        
    #Tests the get request.
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_create.html')

    #Tests the post request.
    def test_post(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_summary.html')
        self.assertTrue(Quiz.objects.filter(name='Test Quiz').exists())

# QuizSummaryViewTest - Tests is the if QuizSumamaryView is working.
#
# Author - Jacob Fielder
class QuizSummaryViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(colored('\nUnitTest is Testing:', 'blue') + colored(' QuizSummaryView', 'red'))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print(colored('View: QuizSummaryView is Tested!', 'green'))

    # Create a Quiz
    def setUp(self):
        self.quiz = Quiz.objects.create(name='Test Quiz')
        self.url = reverse('quiz_summary', args=[self.quiz.id])

    # Check if it returns a 200 code and the template works.
    def test_quiz_summary_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_summary.html')
        self.assertEqual(response.context['quiz'], self.quiz)
        
# SearchQuestionsTest - Tests if the question search is functioning as intended.
#
# Author - Jacob Fielder
class SearchQuestionsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(colored('\nUnitTest is Testing:', 'blue') + colored(' def search_questions(request):', 'red'))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print(colored('DEF: def search_questions(request): is Tested!\n', 'green'))

    def setUp(self):
        self.client = Client()
        self.question1 = Question.objects.create(stem="What is the capital of France?", type=0, explain="Explanation 1")
        self.question2 = Question.objects.create(stem="What is the capital of Spain?", type=0, explain="Explanation 2")

    #test the search.
    def test_search_questions_view(self):
        url = reverse('search_questions')
        response = self.client.get(url, {'stem': 'capital'})
        self.assertEqual(response.status_code, 200)
        expected_data = [
            {'id': self.question1.id, 'stem': self.question1.stem},
            {'id': self.question2.id, 'stem': self.question2.stem},
        ]
        self.assertJSONEqual(response.content, expected_data)

# QuizListView - Tests if the quiz is is listed after creation.
#
# Author - Jacob Fielder
class QuizListViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(colored('\nUnitTest is Testing:', 'blue') + colored('QuizListView:', 'red'))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print(colored('View: QuizListView is Tested!\n', 'green'))
        
    @classmethod
    def setUpTestData(cls):
        # Create some quizzes to test with
        Quiz.objects.create(name='Quiz 1')
        Quiz.objects.create(name='Quiz 2')
        Quiz.objects.create(name='Quiz 3')


    def setUp(self):
        self.client = Client()
        self.url = reverse('quiz_list')

    #Test the get request.
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_list.html')
        expected_quizzes = set(Quiz.objects.all())
        response_quizzes = set(response.context['quizzes'])
        self.assertSetEqual(expected_quizzes, response_quizzes)

    #Test the post request.
    def test_post(self):
        response = self.client.post(self.url, {'query': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_list.html')
        self.assertQuerysetEqual(response.context['quizzes'], Quiz.objects.filter(name__icontains='1'))

