from django.test import TestCase
from post.forms import PostForm
from django.core.files.uploadedfile import SimpleUploadedFile

class TestForm(TestCase):

    def test_post_form(self):
        file = open('test_file/test_article_2.pdf', 'rb')
        file_data = file.read()
        file_name = 'test_article_2.pdf'
        file_type = 'application/pdf'
        uploaded_file = SimpleUploadedFile(file_name, file_data, file_type)
        form = PostForm(data={
            'title': "test tile",
            'description': "test description",
        }, files={'file':uploaded_file})
        file.close()
        self.assertTrue(form.is_valid())

    def test_post_form_blank(self):
        form = PostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)