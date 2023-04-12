# from django.test import TestCase
# from django.urls import reverse
# from .models import fakeMultipleChoiceQuestion

# class questionListViewTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Create 3 questions
#         number_of_questions = 3

#         for question_id in range(number_of_questions):
#             fakeMultipleChoiceQuestion.objects.create(
#                 root=f'What is one plus one?',
#                 correct_answer=f'Two',
#                 distractors=f'Three, Five, Seven',
#                 hint=f'It is odd',
#                 tags=f'Math',
#             )

#     def test_question_page_view_url_exists_at_desired_location(self):
#         response = self.client.get('/questions/')
#         self.assertEqual(response.status_code, 200)

#     def test_question_page_view_url_accessible_by_name(self):
#         response = self.client.get(reverse('questionPage'))
#         self.assertEqual(response.status_code, 200)

#     def test_question_page_view_uses_correct_template(self):
#         response = self.client.get(reverse('questionPage'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'questionPage.html')


#     def test_question_page_lists_all_questions(self):
#         response = self.client.get(reverse('questionPage'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.context['fakemultiplechoicequestion_list']), 3)

   
# class exportTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Create 3 questions
#         number_of_questions = 3

#         for question_id in range(number_of_questions):
#             fakeMultipleChoiceQuestion.objects.create(
#                 root=f'What is one plus one?',
#                 correct_answer=f'Two',
#                 distractors=f'Three, Five, Seven',
#                 hint=f'It is odd',
#                 tags=f'Math',
#             )

#     def test_export_view_url_exists_at_desired_location(self):
#         response = self.client.get('/export_xcl/')
#         self.assertEqual(response.status_code, 200)

#     def test_export_view_url_accessible_by_name(self):
#         response = self.client.get(reverse('export_xcl'))
#         self.assertEqual(response.status_code, 200)


#     def test_export(self):
#         response = self.client.get(reverse('questionPage'))
#         self.assertEqual(response.status_code, 200)
#         data = {'file_format': str("xls")}
#         response = self.client.post('/export_xcl/', data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(response.has_header("Content-Disposition"))
#         self.assertEqual(response['Content-Type'],
#             'application/ms-excel')
#         self.assertEqual(
#             response['Content-Disposition'],
#             'attachment; filename=filename.xls'
#         )
# class importTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Create 3 questions
#         number_of_questions = 3

#         for question_id in range(number_of_questions):
#             fakeMultipleChoiceQuestion.objects.create(
#                 root=f'What is one plus one?',
#                 correct_answer=f'Two',
#                 distractors=f'Three, Five, Seven',
#                 hint=f'It is odd',
#                 tags=f'Math',
#             )

#     def test_import_view_url_exists_at_desired_location(self):
#         response = self.client.get('/questions/importing/')
#         self.assertEqual(response.status_code, 200)

#     def test_import_view_url_accessible_by_name(self):
#         response = self.client.get(reverse('importing'))
#         self.assertEqual(response.status_code, 200)

#     def test_add_view_url_exists_at_desired_location(self):
#         response = self.client.get('/questions/add/')
#         self.assertEqual(response.status_code, 200)

#     def test_add_view_url_accessible_by_name(self):
#         response = self.client.get(reverse('add'))
#         self.assertEqual(response.status_code, 200)


# class deleteButtonTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Create 3 questions
#         number_of_questions = 3

#         for question_id in range(number_of_questions):
#             fakeMultipleChoiceQuestion.objects.create(
#                 root=f'What is one plus one?',
#                 correct_answer=f'Two',
#                 distractors=f'Three, Five, Seven',
#                 hint=f'It is odd',
#                 tags=f'Math',
#             )
#     def test_original_size(self):
#         response = self.client.get(reverse('questionPage'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.context['fakemultiplechoicequestion_list']), 3)
# #Delete a question and test the length to see if it deletes
#     def test_delete_button_view_url_accessible_by_name_and_deletion_works(self):
#         ques = fakeMultipleChoiceQuestion.objects.get(id=1)
#         response = self.client.post(reverse('delete', args=(ques.id,)), follow=True)
#         self.assertRedirects(response, reverse('questionPage'), status_code = 302)
#         response = self.client.get(reverse('questionPage'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.context['fakemultiplechoicequestion_list']), 2)

# class editButtonTest(TestCase):
#     @classmethod
#     def setUpTestData(self):
#         # Create 3 questions
#         number_of_questions = 3
        
#         for question_id in range(number_of_questions):
#             fakeMultipleChoiceQuestion.objects.create(
#                 root=f'What is one plus one?',
#                 correct_answer=f'Two',
#                 distractors=f'Three, Five, Seven',
#                 hint=f'It is odd',
#                 tags=f'Math',
#             )
#     def test_original_size(self):
#         response = self.client.get(reverse('questionPage'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.context['fakemultiplechoicequestion_list']), 3)

# #should not create a new question but alter existing question, so length of question list should stay the same
#     def test_edit_button_view_url_accessible_by_name_and_length_is_same(self):
#         ques = fakeMultipleChoiceQuestion.objects.get(id=1)
#         data = fakeMultipleChoiceQuestion(
#                 root=f'new ques',
#                 correct_answer=f'Two',
#                 distractors=f'Three, Five, Seven',
#                 hint=f'It is odd',
#                 tags=f'Math',
#             )    
#         response = self.client.post(reverse('edit', args=(ques.id,)), request = 'Update', follow=True)
#         response = self.client.get(reverse('questionPage'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.context['fakemultiplechoicequestion_list']), 3)


        
        
#     def test_add_button(self):
#         response = self.client.post("/questions/add/addrecord/", {'root':'something', 'correct_answer':'okay', 'distractors': 'none', 'hint': 'hi','tags':'201'})
#         self.assertEqual(response.status_code, 302)
#         response = self.client.get(reverse('questionPage'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.context['fakemultiplechoicequestion_list']), 4)



        
        
    



        

        
        
        
        

    






    

