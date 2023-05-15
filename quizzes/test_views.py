from django.test import TestCase, Client
from django.urls import reverse
from .forms import questionForm
from .models import Quiz, Question, Tag, Type, User, Student, Teacher, Options, Class, Gradebook
import xlrd
from termcolor import colored   
import os, xlwt, tablib
from xlwt import Workbook
import openpyxl
from django.core.files.uploadedfile import SimpleUploadedFile
import json
from django.utils import timezone

class permutationMultipleChoice(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('Permutation Multiple Choice is Testing: ', 'blue'))
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Permutation Multiple Choice is Tested!', 'green'))
    @classmethod
    def setUpTestData(self):
        
        # Create 1 questions
        ans = Options.objects.create(content = "Data stores, processes, entities, relationships", orderForPerm = '1')
        ans.save()
        ans2 = Options.objects.create(content = "Tables, column names and formats, datat sources, data importing procedures, drill-down procedures", orderForPerm = '2')
        ans2.save()
        op = Options.objects.create(content = "Code look-up tables, foreign keys", orderForPerm = '0')
        op.save()
        op2 = Options.objects.create(content = "Program and file names,access modes, security", orderForPerm = '0')
        op2.save()
        op3 = Options.objects.create(content = "Table names, column names and formats, indexes, views", orderForPerm = '0')
        op3.save()
        op4 = Options.objects.create(content = "Dimensional descriptions, aggregation rules, drill-down procedures", orderForPerm = '0')
        op4.save()
        ques =Question.objects.create(
            stem=f'Which of these best describes the contents of a data dictionary of: a CASE tool, a data warehouse',
            type=1,
            explain=f'No hint',
        )
        ques.save()
        tag1 = Tag.objects.create(tag =f'Software Engineering')
        ques.tag.add(tag1)
        ques.options.add(op, op2, op3, op4)
        ques.correctOption.add(ans, ans2)
        ques.save()

    def test_permutation_question_content(self):
        ques = Question.objects.get(id = 1)
        tempop = ques.options.all()
        tempop2 = ques.correctOption.all()
        temptag = ques.tag.all()
        op = tempop[0]
        optwo = tempop[1]
        opthree = tempop[2]
        opfour = tempop[3]
        ans = tempop2[0]
        ans2 = tempop2[1]
        tag = temptag[0]
        self.assertEqual(ques.stem, 'Which of these best describes the contents of a data dictionary of: a CASE tool, a data warehouse')
        self.assertEqual(ques.type, 1)
        self.assertEqual(ques.explain, 'No hint')
        self.assertEqual(tag.tag, 'Software Engineering')
        self.assertEqual(op.content, 'Code look-up tables, foreign keys')
        self.assertEqual(optwo.content, 'Program and file names,access modes, security')
        self.assertEqual(opthree.content, 'Table names, column names and formats, indexes, views')
        self.assertEqual(opfour.content, 'Dimensional descriptions, aggregation rules, drill-down procedures')
        self.assertEqual(op.orderForPerm, 0)
        self.assertEqual(optwo.orderForPerm, 0)
        self.assertEqual(opthree.orderForPerm, 0)
        self.assertEqual(opfour.orderForPerm, 0)
        self.assertEqual(ans.content, 'Data stores, processes, entities, relationships')
        self.assertEqual(ans2.content, 'Tables, column names and formats, datat sources, data importing procedures, drill-down procedures')
        self.assertEqual(ans.orderForPerm, 1)
        self.assertEqual(ans2.orderForPerm, 2)

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
        self.data = {
            'selectedStudent': ['111111111111', '111111111112', '111111111113'],
            'selectedStudent2': ['111111111112']
        }

        self.c1 = Class.objects.create(name = "CIS-201")

        self.url1 = reverse('addStudentrecord', args=[self.c1.pk])
        self.url2 = reverse('deleteStudentrecord', args=[self.c1.pk])
        
        # creates a teacher for authentication
        User.objects.create(
            id="111222333444",
            is_student=False,
            is_teacher=True,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
            username="test@test.com"
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        self.teacher = Teacher.objects.create(
            user=this_user
        )
        self.teacher.save()

        User.objects.create(id = '111111111111',is_student = True, is_teacher = False,first_name = 'Jasmine', last_name = 'James', email = 'jj@me.com', username = 'jj@me.com')
        studentOneUser = User.objects.get(id = '111111111111')
        studentOneUser.set_password("SlappedHam1233")
        studentOneUser.save()

        User.objects.create(id = '111111111112',is_student = True, is_teacher = False,first_name = 'Belle', last_name = 'Brown', email = 'BelleBrown@me.com', username = 'BelleBrown@me.com')
        studentTwoUser = User.objects.get(id = '111111111112')
        studentTwoUser.set_password("SlappedHam1234")
        studentTwoUser.save()

        User.objects.create(id = '111111111113',is_student = True, is_teacher = False,first_name = 'Snow', last_name = 'Smith', email = 'SS@me.com', username = 'SS@me.com')
        studentThreeUser = User.objects.get(id = '111111111113')
        studentThreeUser.set_password("SlappedHam1235")
        studentThreeUser.save()

        self.s1 = Student.objects.create(user = studentOneUser)
        self.s2 = Student.objects.create(user = studentTwoUser)
        self.s3 = Student.objects.create(user = studentThreeUser)

    def test_num_students_class(self):
        self.assertEqual(len(Student.objects.all().filter(classes=1)), 0)
    
    def test_add_students_to_class(self):
        self.client.login(username="test@test.com", password="SlappedHam123")       # Login as teacher
        response = self.client.post(self.url1, data=self.data)                      # Adds 3 classes to teacher
        self.assertEqual(Student.objects.filter(classes=1).count(), 3)              # Confirm classes added
    
    def test_remove_student_from_class(self):
        self.client.login(username="test@test.com", password="SlappedHam123")       # Login as teacher
        response = self.client.post(self.url1, data=self.data)                      # Adds 3 classes to teacher
        self.assertEqual(Student.objects.filter(classes=1).count(), 3)              # Confirm classes added
        response = self.client.post(self.url2, data=self.data)                      # Removes 1 class from teacher
        self.assertEqual(Student.objects.filter(classes=1).count(), 2)              # Confirm classes removed
    
    def test_remove_specific_student_from_class(self):
        self.client.login(username="test@test.com", password="SlappedHam123")       # Login as teacher
        response = self.client.post(self.url1, data=self.data)                      # Adds 3 classes to teacher
        self.assertEqual(Student.objects.filter(classes=1).count(), 3)              # Confirm classes added
        response = self.client.post(self.url2, data=self.data)                      # Removes 1 class from teacher
        self.assertEqual(Student.objects.filter(classes=1).count(), 2)              # Confirm classes removed
        self.assertTrue(not Student.objects.filter(classes=1).contains(self.s2))    # Confirms specific class removed



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
    @classmethod
    def setUpClass(cls):
        print(colored('Delete Question is Testing: ', 'blue'))
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: Delete Question is Tested!', 'green'))
    @classmethod
    def setUpTestData(self):
        
        # Create 3 questions
        number_of_questions = 3
        count = 1
        ans = Options.objects.create(content = "Correct answer")
        ans.save()
        op = Options.objects.create(content = "fake answer")
        op.save()
        op2 = Options.objects.create(content = "fake answer two")
        op2.save()
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
            ques.options.add(op, op2)
            ques.correctOption.add(ans)
            ques.save()
            count = count + 1
            
        # creates a teacher for authentication
        User.objects.create(
            id="111222333444",
            is_student=False,
            is_teacher=True,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        Teacher.objects.create(
            user=this_user
        )
        teacher = Teacher.objects.all().first()

    def test_question_page_view_url_exists_at_desired_location(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get('/questions/')
        self.assertEqual(response.status_code, 200)

    def test_question_page_view_url_accessible_by_name(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)

    def test_question_page_view_uses_correct_template(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questionPage.html')


    def test_question_page_lists_all_questions(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['question_list']), 3)

    def test_question_content(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        ques = Question.objects.get(id = 1)
        tempop = ques.options.all()
        tempop2 = ques.correctOption.all()
        op = tempop[0]
        optwo = tempop[1]
        ans = tempop2[0]
        self.assertEqual(ques.stem, 'What is one plus one?')
        self.assertEqual(ques.type, 0)
        self.assertEqual(ques.explain, 'It is odd')
        self.assertEqual(op.content, 'fake answer')
        self.assertEqual(optwo.content, 'fake answer two')
        self.assertEqual(ans.content, 'Correct answer')

    def test_second_question_content(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        ques = Question.objects.get(id = 2)
        tempop = ques.options.all()
        tempop2 = ques.correctOption.all()
        op = tempop[0]
        optwo = tempop[1]
        ans = tempop2[0]
        self.assertEqual(ques.stem, 'What is one plus one?')
        self.assertEqual(ques.type, 0)
        self.assertEqual(ques.explain, 'It is odd')
        self.assertEqual(op.content, 'fake answer')
        self.assertEqual(optwo.content, 'fake answer two')
        self.assertEqual(ans.content, 'Correct answer')
    
   
    def test_options_length(self):
        self.assertEqual(len(Options.objects.all()), 3)
    
    def test_options_content(self):
        self.assertEqual(Options.objects.get(id = 1).content, 'Correct answer')
    
    #Delete a question and test the length and if the id exists to see if it deletes
    def test_delete_button_view_url_accessible_by_name_and_deletion_works(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        ques = Question.objects.get(id=1)
        response = self.client.post(reverse('delete', args=(ques.id,)), follow=True)
        self.assertRedirects(response, reverse('questionPage'), status_code = 302)
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['question_list']), 2)
        self.assertFalse(Question.objects.filter(id=1).exists())
        self.assertTrue(Options.objects.filter(pk=1).exists())
       

class editViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('Edit Question is Testing: ', 'blue'))
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: Edit Question is Tested!', 'green'))
    @classmethod
    def setUpClass(cls):
        print(colored('Question Form is Testing: ', 'blue'))
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Model: Question Form is Tested!', 'green'))
    @classmethod
    def setUpTestData(self):
       # Create 1 question
        opt = Options(content="temp")
        opt.save()
        opttwo = Options(content="tempTwo")
        opttwo.save()
        self.question = Question.objects.create(stem="what is two plus two", type=1, explain="two plus two is four.")
        self.question.tag.create(tag='math')
        self.question.options.add(opttwo)
        self.question.correctOption.add(opt)
        self.question.save()
        
        # creates a teacher for authentication
        User.objects.create(
            id="111222333444",
            is_student=False,
            is_teacher=True,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        Teacher.objects.create(
            user=this_user
        )
        teacher = Teacher.objects.all().first()
        
    def test_empty_form(self):
        form = questionForm()        
        self.assertInHTML(      
            '<tr> <th><label for="id_stem">Stem:</label></th> <td> <input type="text" name="stem" maxlength="1024" required id="id_stem"></td></tr><tr><th><label for="id_type">Type:</label></th><td><select name="type" required id="id_type"><option value="" selected>---------</option><option value="0">MC</option><option value="1">PMC</option><option value="2">PP</option></select></td></tr><tr><th><label for="id_explain">Explain:</label></th><td><input type="text" name="explain" maxlength="512" required id="id_explain"></td></tr><tr><th><label for="id_tag">Tag:</label></th><td><select name="tag" id="id_tag" multiple><option value="1">math</option></select></td></tr><tr><th><label for="id_options">Options:</label></th><td><select name="options" required id="id_options" multiple><option value="1">temp</option><option value="2">tempTwo</option></select></td></tr><tr><th><label for="id_correctOption">CorrectOption:</label></th><td><select name="correctOption" required id="id_correctOption" multiple><option value="1">temp</option><option value="2">tempTwo</option></select></td></tr>', str(form)
        )
    def test_valid_form(self):
        opt = Options(content="other")
        opt.save()
        opttwo = Options(content="otherTwo")
        opttwo.save()
        ques= Question.objects.create(stem="newQues", type=2, explain="new hint")
        ques.tag.create(tag='example')
        ques.options.add(opttwo)
        ques.correctOption.add(opt)
        ques.save()
        data = {
            'stem': ques.stem, 
            'type': ques.type,
            'explain': ques.explain,
            'correctOption': ques.correctOption.all(),
            'options': ques.options.all(),
            'tag':ques.tag.all(),
        }
        form = questionForm(data=data)
        self.assertTrue(form.is_valid())
    #testing invalid form by leaving out field
    def test_invalid_form(self):
        opt = Options(content="other")
        opt.save()
        opttwo = Options(content="otherTwo")
        opttwo.save()
        ques= Question.objects.create(stem="newQues", type=2, explain="new hint")
        ques.tag.create(tag='example')
        ques.options.add(opttwo)
        ques.correctOption.add(opt)
        ques.save()
        data = {
            'stem': ques.stem, 
            'type': ques.type,
            'correctOption': ques.correctOption.all(),
            'options': ques.options.all(),
            'tag':ques.tag.all(),
        }
        form = questionForm(data=data)
        self.assertFalse(form.is_valid()) 

    # #should not create a new question but alter existing question, so length of question list should stay the same
    def test_edit_button_view_url_accessible_by_name_and_length_is_same(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        opt = Options(content="other")
        opt.save()
        opttwo = Options(content="otherTwo")
        opttwo.save()
        ques= Question.objects.create(stem="newQues", type=2, explain="new hint")
        ques.tag.create(tag='example')
        ques.options.add(opttwo)
        ques.correctOption.add(opt)
        ques.save()
        self.assertEqual(ques.stem, "newQues")
        data = {
            'stem': "What is an apple?", 
            'type': ques.type,
            'explain': ques.explain,
            'correctOption': ques.correctOption.all(),
            'options': ques.options.all(),
            'tag':ques.tag.all(),
        }
        # form = questionForm(data=data)
        # self.assertTrue(form.is_valid())
        response = self.client.post(reverse("edit", args=[ques.id]),Update = 'Update', data = data)
        # response = self.client.post(url = 'edit', path = '/questions/edit_question/1',data = data)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['question_list']), 2)
        # ques.refresh_from_db()
        # self.assertEqual(ques.stem, "What is an apple?")
   
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
        opt1 = Options.objects.create(content = "one")
        opt1.save()
        opt2 = Options.objects.create(content = "two")
        opt2.save()
        opt3 = Options.objects.create(content = "three")
        opt3.save()
        self.ques =Question.objects.create(
            stem=f'What is one plus one?',
            type=0,
            explain=f'It is even'
        )
        tag1 = Tag.objects.create(tag =f'CIS201')
        tag2 = Tag.objects.create(tag =f'CIS202')
        self.ques.tag.add(tag1, tag2)
        self.ques.options.add(opt1, opt3)
        self.ques.correctOption.add(opt2)
        self.ques =Question.objects.create(
            stem=f'What is one plus zero?',
            type=0,
            explain=f'It is odd'
        )
        tag1 = Tag.objects.create(tag =f'CIS201')
        tag2 = Tag.objects.create(tag =f'CIS202')
        self.ques.tag.add(tag1, tag2)
        self.ques.options.add(opt2, opt3)
        self.ques.correctOption.add(opt1)
        self.ques =Question.objects.create(
            stem=f'What is one plus two?',
            type=0,
            explain=f'It is odd'
        )
        tag1 = Tag.objects.create(tag =f'CIS201')
        tag2 = Tag.objects.create(tag =f'CIS202')
        self.ques.tag.add(tag1, tag2)
        self.ques.options.add(opt1, opt2)
        self.ques.correctOption.add(opt3)
        
        # creates a teacher for authentication
        User.objects.create(
            id="111222333444",
            is_student=False,
            is_teacher=True,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        Teacher.objects.create(
            user=this_user
        )
        teacher = Teacher.objects.all().first()

    def test_export_view_url_exists_at_desired_location(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get('/export_xcl/')
        self.assertEqual(response.status_code, 200)

    def test_export_view_url_accessible_by_name(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get(reverse('export_xcl'))
        self.assertEqual(response.status_code, 200)
    def test_export_question_page_lists_all_questions(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['question_list']), 3)

    def test_export(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
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



class addPageTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('Add Page is Testing: ', 'blue'))
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n View: Add Page is Tested!', 'green'))
    @classmethod
    def setUpTestData(self):
        # Create 3 questions
        
        opt1 = Options.objects.create(content = "five")
        opt1.save()
        opt2 = Options.objects.create(content = "seven")
        opt2.save()
        opt3 = Options.objects.create(content = "nine")
        opt3.save()
        opt4 = Options.objects.create(content = "eleven")
        opt4.save()
        self.ques =Question.objects.create(
            stem='What is two plus three?',
            type=1,
            explain="it's not four"
        )
        tag1 = Tag.objects.create(tag ='Math')
        tag2 = Tag.objects.create(tag ='Addition')
        self.ques.tag.add(tag1, tag2)
        self.ques.options.add(opt1, opt2, opt3, opt4)
        self.ques.correctOption.add(opt1)
        self.ques =Question.objects.create(
            stem='What is three plus four?',
            type=1,
            explain='eight minus one'
        )
        tag1 = Tag.objects.create(tag ='Math')
        tag2 = Tag.objects.create(tag ='Addition')
        self.ques.tag.add(tag1, tag2)
        self.ques.correctOption.add(opt2)
        self.ques.options.add(opt1, opt2, opt3, opt4)
        self.ques =Question.objects.create(
            stem='What is what is three times three?',
            type=1,
            explain='same as three plus three plus three'
        )
        tag1 = Tag.objects.create(tag ='Math')
        tag2 = Tag.objects.create(tag ='Multiplication')
        self.ques.correctOption.add(opt3)
        self.ques.tag.add(tag1, tag2)
        self.ques.options.add(opt1, opt2, opt3, opt4)
        
        # creates a teacher for authentication
        User.objects.create(
            id="111222333444",
            is_student=False,
            is_teacher=True,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        Teacher.objects.create(
            user=this_user
        )
        teacher = Teacher.objects.all().first()
        
            
    def test_add_page_view_url_exists_at_desired_location(self):
        # print("Tested Add Page View exists at the correct URL.")
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get('/questions/add/')
        self.assertEqual(response.status_code, 200)

    def test_add_page_view_url_accessible_by_name(self):
        # print("Tested that Add Page URL is accessible by name.")
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)

    def test_add_page_view_uses_correct_template(self):
        # print("Tested that Add Page URL uses the correct template.")
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add.html')  
    
    def test_add_and_submit_button(self):
        # print("Tested the 'Add and Submit' Button.")
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(len(response.context['question_list']), 3)
        #tested adding a permutation question(mult answers)
        response = self.client.post("/questions/add/addrecord/", {'stem':'something', 'type':1, 'explain': 'none', 'tag': 'hi|bye', 'options':'opt1:@0|opt2:@2|correct:@1', 'correctOption':'correct:@1|opt1:@2', 'Submit':'Submit'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['question_list']), 4)
    
    def test_submit_and_add_another_button(self):
        # print("Tested the 'Submit and Add Another' Button.")
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.post("/questions/add/addrecord/", {'stem':'something else', 'type':0, 'explain': 'explaination here', 'tag': 'bye', 'options':'opt1:@0|opt2:@0', 'correctOption':'correct:@0', 'Submit':'Submit'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('add'))
        response = self.client.post("/questions/add/addrecord/", {'stem':'another question stem', 'type':0, 'explain': 'explaination2 here', 'tag': 'tag1|tag2', 'options': 'opt:@01|opt2:@0', 'correctOption':'correct:@0', 'Submit':'Submit'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['question_list']), 5)


    def test_cancel_button(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get("/questions/add/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['question_list']), 3)
    
    
class importTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('Import is Testing: ', 'blue'))
        super().setUpClass()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n View: Import is Tested!', 'green'))
    @classmethod
    def setUpTestData(self):
        print(colored('View testing: ', 'blue')+colored('Import', 'red'))
        
        # Create 3 questions
        opt1 = Options.objects.create(content = "five")
        opt1.save()
        opt2 = Options.objects.create(content = "seven")
        opt2.save()
        opt3 = Options.objects.create(content = "nine")
        opt3.save()
        opt4 = Options.objects.create(content = "eleven")
        opt4.save()
        self.ques =Question.objects.create(
            stem='What is two plus three?',
            type=1,
            explain="it's not four"
        )
        tag1 = Tag.objects.create(tag ='Math')
        tag2 = Tag.objects.create(tag ='Addition')
        self.ques.tag.add(tag1, tag2)
        self.ques.options.add(opt1, opt2, opt3, opt4)
        self.ques.correctOption.add(opt1)
        self.ques =Question.objects.create(
            stem='What is three plus four?',
            type=1,
            explain='eight minus one'
        )
        tag1 = Tag.objects.create(tag ='Math')
        tag2 = Tag.objects.create(tag ='Addition')
        self.ques.tag.add(tag1, tag2)
        self.ques.options.add(opt1, opt2, opt3, opt4)
        self.ques.correctOption.add(opt2)
        self.ques =Question.objects.create(
            stem='What is what is three times three?',
            type=1,
            explain='same as three plus three plus three'
        )
        tag1 = Tag.objects.create(tag ='Math')
        tag2 = Tag.objects.create(tag ='Multiplication')
        self.ques.tag.add(tag1, tag2)
        self.ques.correctOption.add(opt3)
        self.ques.options.add(opt1, opt2, opt3, opt4)
        
        # creates a teacher for authentication
        User.objects.create(
            id="111222333444",
            is_student=False,
            is_teacher=True,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        Teacher.objects.create(
            user=this_user
        )
        teacher = Teacher.objects.all().first()
        
        
    def test_import_view_url_exists_at_desired_location(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get('/questions/importing/')
        self.assertEqual(response.status_code, 200)

    def test_import_view_url_accessible_by_name(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get(reverse('importing'))
        self.assertEqual(response.status_code, 200)

        
    def test_importing_file(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get(reverse('questionPage'))
        
        # create file to import
        wb = Workbook()
        sheet = wb.add_sheet('Sheet 1')
        sheet.write(0, 0, 'ID')
        sheet.write(0, 1, 'Question')
        sheet.write(0, 2, 'Type')
        sheet.write(0, 3, 'Answer')
        sheet.write(0, 4, 'Options')
        sheet.write(0, 5, 'Hint')
        sheet.write(0, 6, 'Tags')
        sheet.write(1, 0, '4')
        sheet.write(1, 1, 'What does // mean?')
        sheet.write(1, 2, 'PP')
        sheet.write(1, 3, 'a single line comment')
        sheet.write(1, 4, 'multi-line|single line|no line|idk')
        sheet.write(1, 5, 'it is a type of comment')
        sheet.write(1, 6, 'Java|CIS')
        wb.save('import_test_file.xls')
        
        # file = {'my_file':'import_test_form.xls'}
        # response = self.client.post(reverse('importing'), file)
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'import_form.html')
        
        # response = self.client.post(reverse('importxcl'))
        # self.assertEqual(response.status_code, 200)
        # response = self.client.get(reverse('questionPage'))
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.context['question_list']), 4)
        


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
        response = self.client.get(reverse('index'))#, kwargs={'student_id': student.user.id}
        # Redirects to the login page as intended - hence 302 status code
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        this_user = User.objects.all().first()
        student = Student.objects.all().first()
        self.client.login(username="test@test.com", password="SlappedHam123")
        
        response = self.client.get(reverse('index'))#, kwargs={'student_id': student.user.id}
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
            'passingThreshold': 65
        }
        
        # creates a teacher for authentication
        User.objects.create(
            id="111222333444",
            is_student=False,
            is_teacher=True,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        Teacher.objects.create(
            user=this_user
        )
        teacher = Teacher.objects.all().first()
        
    #Tests the get request.
    def test_get(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_create.html')

    #Tests the post request.
    def test_post(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
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
        gb = Gradebook()
        gb.save()
        self.quiz = Quiz.objects.create(name='Test Quiz', gradebook = gb)
        self.url = reverse('quiz_summary', args=[self.quiz.id])
        
        # creates a teacher for authentication
        User.objects.create(
            id="111222333444",
            is_student=False,
            is_teacher=True,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        Teacher.objects.create(
            user=this_user
        )
        teacher = Teacher.objects.all().first()

    # Check if it returns a 200 code and the template works.
    def test_quiz_summary_view(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
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
        opt1 = Options.objects.create(content = "one")
        opt1.save()
        opt2 = Options.objects.create(content = "two")
        opt2.save()
        self.question1 = Question.objects.create(stem="What is the capital of France?", type=0, explain="Explanation 1")
        self.question1.correctOption.add(opt1)
        self.question2 = Question.objects.create(stem="What is the capital of Spain?", type=0, explain="Explanation 2")
        self.question2.correctOption.add(opt2)
        # creates a teacher for authentication
        User.objects.create(
            id="111222333444",
            is_student=False,
            is_teacher=True,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        Teacher.objects.create(
            user=this_user
        )
        teacher = Teacher.objects.all().first()

    #test the search.
    def test_search_questions_view(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
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
        gb1 = Gradebook()
        gb1.save()
        Quiz.objects.create(name='Quiz 1', gradebook = gb1)
        gb2 = Gradebook()
        gb2.save()
        Quiz.objects.create(name='Quiz 2', gradebook = gb2)
        gb3 = Gradebook()
        gb3.save()
        Quiz.objects.create(name='Quiz 3', gradebook = gb3)


    def setUp(self):
        self.client = Client()
        self.url = reverse('quiz_list')
        
        # creates a teacher for authentication
        User.objects.create(
            id="111222333444",
            is_student=False,
            is_teacher=True,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        Teacher.objects.create(
            user=this_user
        )
        teacher = Teacher.objects.all().first()

    #Test the get request.
    def test_get(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_list.html')
        expected_quizzes = set(Quiz.objects.all())
        response_quizzes = set(response.context['quizzes'])
        self.assertSetEqual(expected_quizzes, response_quizzes)

    #Test the post request.
    def test_post(self):
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.post(self.url, {'query': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_list.html')
        self.assertQuerysetEqual(response.context['quizzes'], Quiz.objects.filter(name__icontains='1'))

# Test for ensuring the created quiz is assigned to a class
# 
# There were a lot of issues constructing this
# test stemming from the ManyToMany field in the
# Class model that contains the quizzes
# 
# Because of this, I have no idea how I fixed it
# It works so I'm not complaining
class QuizToClassRelationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(colored('\nUnitTest is Testing:', 'blue') + colored(' QuizToClassRelation', 'red'))


    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print(colored('View: QuizToClassRelation is Tested!', 'green'))

    def setUp(self):
        self.client = Client()

        # Creation of filler information to get the m2m field working
        gb = Gradebook.objects.create()
        gb.save()

        filler = Quiz.objects.create(name="filler", gradebook = gb)
        filler.save()

        self.cl = Class.objects.create(name = "Test Class")
        self.cl.quizzes.add(filler)
        self.cl.save()

        # I decided to use Jacob's test to ensure that it works through the creation form
        self.url = reverse('quiz_create')
        self.data = {
            'quiz_name': 'Test Quiz',
            'start_time': timezone.localtime().strftime('%Y-%m-%dT%H:%M'),
            'end_time': (timezone.localtime() + timezone.timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M'),
            'stem': 'test',
            'questions': ['test question'],
            'passingThreshold': 65,
            'selectedClass': [self.cl.pk]
        }
        
        # creates a teacher for authentication
        User.objects.create(
            id="111222333444",
            is_student=False,
            is_teacher=True,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        Teacher.objects.create(
            user=this_user
        )
        self.teacher = Teacher.objects.all().first()
        self.teacher.classes.add(self.cl)
        self.teacher.save()

    # A simple test just to ensure that the passingThreshold is added appropraitely
    def test_quiz_passing_threshold_exists(self):
        self.client.login(username="test@test.com", password="SlappedHam123")       # Login as teacher
        response = self.client.post(self.url, data=self.data)                       # Create the quiz
        self.assertEqual(response.status_code, 200)                                 # Confirm the redirect page
        self.assertTemplateUsed(response, 'quiz_summary.html')                      # Ensure it redirected correctly
        self.assertEqual(Quiz.objects.get(name='Test Quiz').passingThreshold, 65)   # Checks the passing threshold

    # The big test that caused 3 ******* hours of bug testing
    # FOR 3 LINES OF CODE????? The solution was stupid too
    # So stupid that I have no idea what it actually was
    # I have like 2 or 3 theories, but I'm not sure which is right
    def test_quiz_added_to_class(self):
        self.client.login(username="test@test.com", password="SlappedHam123")       # Login as teacher
        response = self.client.post(self.url, data=self.data)                       # Create the quiz
        self.assertTrue(self.cl.quizzes.get(name='Test Quiz'))                      # Test if the quiz is in the class


# Test for checking grade saving interactions
# 
# This one went a lot better
# 
# It's long, but pretty straight forward
# See comments below for details
class TakeQuizTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(colored('\nUnitTest is Testing:', 'blue') + colored(' TakeQuiz', 'red'))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print(colored('View: TakeQuiz is Tested!', 'green'))

    def setUp(self):
        self.client = Client()

        # Creation of filler information to get the m2m field working
        gb = Gradebook.objects.create()
        gb.save()
        filler = Quiz.objects.create(name="filler", gradebook = gb)
        filler.save()
        self.cl = Class.objects.create(name = "Test Class")
        self.cl.quizzes.add(filler)
        self.cl.save()

        # Options for the only question in the quiz
        o1 = Options.objects.create(content="answer1")
        o1.save()
        o2 = Options.objects.create(content="answer2")
        o2.save()
        o3 = Options.objects.create(content="answer3")
        o3.save()
        question = Question.objects.create(stem = "example", type = 0)
        question.correctOption.add(o1)
        question.options.add(o1)
        question.options.add(o2)
        question.options.add(o3)
        question.save()

        # Once again I figured I should include Jacob's test just to make sure everything works together 
        self.url = reverse('quiz_create')
        self.data = {
            'quiz_name': 'Test Quiz',
            'start_time': timezone.localtime().strftime('%Y-%m-%dT%H:%M'),
            'end_time': (timezone.localtime() + timezone.timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M'),
            'stem': 'test',
            'questions': ['example'],
            'question_ids[]': [question.pk],
            'passingThreshold': 65,
            'selectedClass': [1]
        }

        # creates a student to take the quiz
        User.objects.create(
            id="999999999999",
            is_student=True,
            is_teacher=False,
            first_name="Richie",
            last_name="Guy",
            email="richieman@test.com",
            username="richieman@test.com"
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        Student.objects.create(
            user=this_user
        )
        self.student = Student.objects.all().first()
        self.student.classes.add(self.cl)
        self.student.save()

        # creates a teacher for authentication
        User.objects.create(
            id="111222333444",
            is_student=False,
            is_teacher=True,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
            username="test@test.com"
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        Teacher.objects.create(
            user=this_user
        )
        self.teacher = Teacher.objects.all().first()
        self.teacher.classes.add(self.cl)
        self.teacher.save()

    # A simple test to make sure that a student has access to a newly created quiz
    def test_student_access_quiz(self):
        self.client.login(username="test@test.com", password="SlappedHam123")       # Login as teacher
        response = self.client.post(self.url, data=self.data)                       # Create the quiz
        self.assertEqual(response.status_code, 200)                                 # Confirm the redirect page
#                                                                                   #
        self.client.login(username="richieman@test.com", password="SlappedHam123")  # Login as student
        self.quiz_url = reverse('take_quiz', kwargs={                               # Retrieves the url
            'quiz_id':Quiz.objects.get(name='Test Quiz').pk                         # for taking the quiz
            })                                                                      # at the specified pk
#                                                                                   #
        self.quiz_data = {                                                          # Passes one answer
            'selectedOpt': "1:1"                                                    # for the question
        }                                                                           # 
#                                                                                   #
        response2 = self.client.get(self.quiz_url)                                  # Accesses the quiz page
        self.assertEqual(response2.status_code, 200)                                # Ensures no redirect

    # Tests if the grade is stored in the gradebook
    def test_student_answers_saved_in_gradebook(self):
        self.client.login(username="test@test.com", password="SlappedHam123")       # Login as teacher
        response = self.client.post(self.url, data=self.data)                       # Create the quiz
        self.assertEqual(response.status_code, 200)                                 # Confirm the redirect page
#                                                                                   #
        self.client.login(username="richieman@test.com", password="SlappedHam123")  # Login as student
        self.quiz_url = reverse('submitQuiz', kwargs={                              # Retrieves the url
            'quiz_id':Quiz.objects.get(name='Test Quiz').pk                         # for taking the quiz
            })                                                                      # at the specified pk
#                                                                                   #
        self.quiz_data = {                                                          # Passes one answer
            'selectedOpt': "1:1"                                                    # for the question
        }                                                                           # 
#                                                                                   #
        response2 = self.client.post(self.quiz_url, data=self.quiz_data)            # Accesses the quiz page
        self.assertEqual(response2.status_code, 200)                                # Ensures no redirect
        quiz = Quiz.objects.get(name='Test Quiz')                                   # Retrieve quiz
        self.assertEqual(                                                           # Ensures the following are equal
            quiz.gradebook.student_data.get(student_id=999999999999).grade,         # Saved grade in gradebook
            100)                                                                    # Expected grade
        
        
# Tests to see if a user can reset their password
class PasswordResetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('Password reset is Testing: ', 'blue'))
        super().setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n view: Password reset is Tested!', 'green'))
        
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

    def test_password_reset(self):
        # login as created student
        self.client.login(username="test@test.com", password="SlappedHam123")
        response = self.client.get(reverse('resetPassword'))
        self.assertEqual(response.status_code, 200)
        # enters the user's old password, new password, and new password again for confirmation
        self.client.post('password_reset/', {"password_old": "SlappedHam123", "password1": "12345SlappedHam", "password2": "12345SlappedHam"})
        self.assertEqual(response.status_code, 200)
        # login as the student using the new password
        self.client.login(username="test@test.com", password="12345SlappedHam")
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        
        
# Tests to see if an admin can reset a user's password
class AdminPasswordResetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('Admin password reset is Testing: ', 'blue'))
        super().setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n view: Admin password reset is Tested!', 'green'))
        
    @classmethod
    def setUp(self):
        # create a student
        User.objects.create(
            id="111222333444",
            is_student=True,
            is_teacher=False,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
            username="test@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        Student.objects.create(
            user=this_user
        )
        student = Student.objects.all().first()
        
        # create a teacher with admin privilages
        User.objects.create(
            id="444333222111",
            is_student=False,
            is_teacher=True,
            first_name="L.",
            last_name="Grabowski",
            email="grabowski@test.com",
            username="grabowski@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        this_user.is_staff = True
        this_user.is_superuser = True
        this_user.save()
        Teacher.objects.create(
            user=this_user
        )
        teacher = Teacher.objects.all().first()

    def test_admin_password_reset(self):
        # login as the created teacher
        self.client.login(username="grabowski@test.com", password="SlappedHam123")
        response = self.client.get(reverse('adminPasswordReset'))
        self.assertEqual(response.status_code, 302)
        # enter the created student's email, new password, and new password confirmation
        self.client.post('quiz_home/admin_password_reset/', {"email": "test@test.com", "password1": "12345SlappedHam", "password2": "12345SlappedHam"})
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        # login as student to check if the password change was successful
        self.client.login(username="test@test.com", password="12345SlappedHam")
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        
        
# Tests to see if an admin can toggle between student and teacher views
class AdminViewToggleTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('Admin view toggle is Testing: ', 'blue'))
        super().setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n view: Admin view toggle is Tested!', 'green'))
        
    @classmethod
    def setUp(self):
        # create a teacher with admin privilages
        User.objects.create(
            id="444333222111",
            is_student=False,
            is_teacher=True,
            first_name="L.",
            last_name="Grabowski",
            email="grabowski@test.com",
            username="grabowski@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        this_user.is_staff = True
        this_user.is_superuser = True
        this_user.save()
        Teacher.objects.create(
            user=this_user
        )
        teacher = Teacher.objects.all().first()

    def test_admin_password_reset(self):
        # login as the created teacher
        self.client.login(username="grabowski@test.com", password="SlappedHam123")
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        # test if adminViewChange will switch the user to the student view
        response = self.client.get(reverse('adminViewChange', kwargs={"view_id": "student"}))
        self.assertEqual(response.status_code, 302)
        this_user = User.objects.get(id='444333222111')
        self.assertEqual(this_user.is_student, True)
        self.assertEqual(this_user.is_teacher, False)
        # test if adminViewChange will switch the user back to the teacher view
        response = self.client.get(reverse('adminViewChange', kwargs={"view_id": "teacher"}))
        self.assertEqual(response.status_code, 302)
        this_user = User.objects.get(id='444333222111')
        self.assertEqual(this_user.is_teacher, True)
        self.assertEqual(this_user.is_student, False)
        
        

class CreateClassTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('Create Class Function is Testing: ', 'blue'))
        super().setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Create Class Function is Tested!', 'green'))
        
    @classmethod
    def setUp(self):
        self.url = reverse('create_class')
        self.data = {
            'name': 'CIS-405'
        }
        
        # creates a teacher for authentication
        User.objects.create(
            id="111222333444",
            is_student=False,
            is_teacher=True,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        Teacher.objects.create(
            user=this_user
        )

    def test_create_class_redirect(self):
        self.client.login(username="test@test.com", password="SlappedHam123")       # Login as teacher
        response = self.client.post(self.url, data=self.data)                       # Create the class
        self.assertEqual(response.status_code, 301)                                 # Confirm redirect to home page

    def test_create_class(self):
        self.client.login(username="test@test.com", password="SlappedHam123")       # Login as teacher
        response = self.client.post(self.url, data=self.data)                       # Create the class
        self.assertEqual(response.status_code, 301)                                 # Confirm redirect to home page
        self.assertTrue(Class.objects.filter(name="CIS-405").count() == 1)          # Confirms the class exists



class AddDropClassTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('Add/Drop Classes is Testing: ', 'blue'))
        super().setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Add/Drop Classes is Tested!', 'green'))
        
    @classmethod
    def setUp(self):
        self.url1 = reverse('addClass')
        self.url2 = reverse('dropClass')
        self.data = {
            'selectedClass': ['1', '2', '3'],
            'selectedClass2': ['2']
        }

        self.c1 = Class.objects.create(name = "CIS-201")
        self.c2 = Class.objects.create(name = "CIS-203")
        self.c3 = Class.objects.create(name = "CIS-300")
        
        # creates a teacher for authentication
        User.objects.create(
            id="111222333444",
            is_student=False,
            is_teacher=True,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        self.teacher = Teacher.objects.create(
            user=this_user
        )
        self.teacher.save()

    def test_add_classes(self):
        self.client.login(username="test@test.com", password="SlappedHam123")       # Login as teacher
        response = self.client.post(self.url1, data=self.data)                      # Adds 3 classes to teacher
        self.assertEqual(self.teacher.classes.count(), 3)                           # Confirm classes added

    def test_remove_classes(self):
        self.client.login(username="test@test.com", password="SlappedHam123")       # Login as teacher
        response = self.client.post(self.url1, data=self.data)                      # Adds 3 classes to teacher
        self.assertEqual(self.teacher.classes.count(), 3)                           # Confirm classes added
        response = self.client.post(self.url2, data=self.data)                      # Removes 1 class from teacher
        self.assertEqual(self.teacher.classes.count(), 2)                           # Confirm classes removed

    def test_remove_specific_class(self):
        self.client.login(username="test@test.com", password="SlappedHam123")       # Login as teacher
        response = self.client.post(self.url1, data=self.data)                      # Adds 3 classes to teacher
        self.assertEqual(self.teacher.classes.count(), 3)                           # Confirm classes added
        response = self.client.post(self.url2, data=self.data)                      # Removes 1 class from teacher
        self.assertEqual(self.teacher.classes.count(), 2)                           # Confirm classes removed
        self.assertTrue(not self.teacher.classes.contains(self.c2))                 # Confirms specific class removed



class AddRemoveStudentsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print(colored('Add/Drop Classes is Testing: ', 'blue'))
        super().setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("/"+colored('\n Add/Drop Classes is Tested!', 'green'))
        
    @classmethod
    def setUp(self):
        self.url1 = reverse('addClass')
        self.url2 = reverse('dropClass')
        self.data = {
            'selectedClass': ['1', '2', '3'],
            'selectedClass2': ['2']
        }

        self.c1 = Class.objects.create(name = "CIS-201")
        self.c2 = Class.objects.create(name = "CIS-203")
        self.c3 = Class.objects.create(name = "CIS-300")
        
        # creates a teacher for authentication
        User.objects.create(
            id="111222333444",
            is_student=False,
            is_teacher=True,
            first_name="Richie",
            last_name="Guy",
            email="test@test.com",
        )
        this_user = User.objects.all().first()
        this_user.set_password("SlappedHam123")
        this_user.save()
        self.teacher = Teacher.objects.create(
            user=this_user
        )
        self.teacher.save()

    def test_add_classes(self):
        self.client.login(username="test@test.com", password="SlappedHam123")       # Login as teacher
        response = self.client.post(self.url1, data=self.data)                      # Adds 3 classes to teacher
        self.assertEqual(self.teacher.classes.count(), 3)                           # Confirm classes added

    def test_remove_classes(self):
        self.client.login(username="test@test.com", password="SlappedHam123")       # Login as teacher
        response = self.client.post(self.url1, data=self.data)                      # Adds 3 classes to teacher
        self.assertEqual(self.teacher.classes.count(), 3)                           # Confirm classes added
        response = self.client.post(self.url2, data=self.data)                      # Removes 1 class from teacher
        self.assertEqual(self.teacher.classes.count(), 2)                           # Confirm classes removed

    def test_remove_specific_class(self):
        self.client.login(username="test@test.com", password="SlappedHam123")       # Login as teacher
        response = self.client.post(self.url1, data=self.data)                      # Adds 3 classes to teacher
        self.assertEqual(self.teacher.classes.count(), 3)                           # Confirm classes added
        response = self.client.post(self.url2, data=self.data)                      # Removes 1 class from teacher
        self.assertEqual(self.teacher.classes.count(), 2)                           # Confirm classes removed
        self.assertTrue(not self.teacher.classes.contains(self.c2))                 # Confirms specific class removed