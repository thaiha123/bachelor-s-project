from django.test import TestCase
from main.forms import user_edit_form, UserCreationForm, profile_edit_form
from django.core.files.uploadedfile import SimpleUploadedFile

class TestForm(TestCase):
    '''
    def test_user_creation_form_valid(self):
        form = UserCreationForm(data={
            'username': 'testuser',
            'email': 'test@mail.com',
            'password1': 'Testpass123',
            'password2': 'Testpass123',
        })
        self.assertTrue(form.is_valid())

    def test_user_edit_form_valid(self):
        form = user_edit_form(data={
            'username': 'testuser',
            'email': 'test@mail.com',
        })
        self.assertTrue(form.is_valid())

    def test_profile_edit_form_valid(self):
        pic = open('test_file/test_pic.jpg', 'rb')
        file_data = pic.read()
        file_name = 'test_article_2.pdf'
        file_type = 'application/pdf'
        uploaded_file = SimpleUploadedFile(file_name, file_data, file_type)
        form = profile_edit_form(data={
            'work_at': 'test work place',
            'intro': 'test introduction',
        }, files={'profile_pic': uploaded_file})
        pic.close()
        self.assertTrue(form.is_valid())        

    def test_user_creation_from_blank(self):
        form = UserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_user_edit_from_blank(self):
        form = user_edit_form(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_profile_edit_from_blank(self):
        form = profile_edit_form(data={})
        self.assertTrue(form.is_valid())
    '''