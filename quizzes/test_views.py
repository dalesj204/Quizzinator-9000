from django.test import TestCase
from django.urls import reverse

from quizzes.forms import questionForm
from .models import Question, Tag, Option, Type
import xlrd
from termcolor import colored   
import os, xlwt, tablib
from xlwt import Workbook
import openpyxl
from django.core.files.uploadedfile import SimpleUploadedFile
class questionListViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        print("Question list is Testing")
        print("Question list Tested!")
        # Create 3 questions
        number_of_questions = 3

        for question_id in range(number_of_questions):
            self.ques =Question.objects.create(
                stem=f'What is one plus one?',
                type=0,
                explain=f'It is odd',
            )
            tag1 = Tag.objects.create(tag =f'CIS201')
            tag2 = Tag.objects.create(tag =f'CIS202')
            self.ques.tag.add(tag1, tag2)
            

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
        
        

    #Delete a question and test the length and if the id exists to see if it deletes
    def test_delete_button_view_url_accessible_by_name_and_deletion_works(self):
        print("Delete button is Testing")
        ques = Question.objects.get(id=1)
        response = self.client.post(reverse('delete', args=(ques.id,)), follow=True)
        self.assertRedirects(response, reverse('questionPage'), status_code = 302)
        response = self.client.get(reverse('questionPage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['question_list']), 2)
        self.assertFalse(Question.objects.filter(pk=1).exists())
        print("Delete button Tested!")

class editViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        print("Edit question is Testing")
        print("Edit question Tested!")
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
    def setUpTestData(self):
        print("Exporting is Testing")
        print("Exporting Tested!")
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