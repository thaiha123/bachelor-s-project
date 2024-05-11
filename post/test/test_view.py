from django.test import TestCase, Client
from django.urls import reverse
from post.models import Post, Tag
from main.models import User, Profile
from django.core.files import File

class TestViews(TestCase):
    
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='testpass')
        self.test_profile = Profile.objects.create(user = self.test_user)
        test_file = open('test_file/test_article_1.pdf', 'rb')
        self.test_post1 = Post.objects.create(author = self.test_user, title='test post1', description='This is a test post 1', file=File(test_file))
        test_file.close()
        test_file = open('test_file/test_article_3.pdf', 'rb')
        self.test_post2 = Post.objects.create(author = self.test_user, title='test post2', description='This is a test post 2', file=File(test_file))
        test_file.close()
        self.test_tag = Tag.objects.create(name='test tag')
        self.test_tag.post.add(self.test_post1)
        
        self.client = Client()
        self.client.login(username='testuser', password='testpass')
    
    def test_create_post_get(self):
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/create_post.html')
    
    def test_view_post_get(self):
        response = self.client.get(reverse('view_post', kwargs={'post_id':self.test_post1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/view_post.html')
     
    def test_edit_post_get(self):
        response = self.client.get(reverse('edit_post', kwargs={'post_id':self.test_post1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/edit_post.html')
    
    def test_compare_get(self):
        response = self.client.get(reverse('compare'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/compare.html')

    def test_delete_get(self):
        response = self.client.get(reverse('delete', kwargs={'post_id':self.test_post1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('main/profile.html')
        self.assertFalse(Post.objects.filter(id=self.test_post1.pk).exists())
    
    def test_create_post_post(self):
        file = open('test_file/test_article_2.pdf', 'rb')
        response = self.client.post(reverse('create_post'), {
            'title': 'new_article',
            'description': 'description for new article',
            'file': file,
        })
        file.close()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='new_article').exists())
        self.assertTemplateUsed('main/home.html')
    
    def test_edit_post_post(self):
        file = open('test_file/test_article_2.pdf', 'rb')
        response = self.client.post(reverse('edit_post', kwargs={'post_id':self.test_post1.pk}), {
            'title': 'test post edited',
            'description': 'this is a test post edited',
            'file': file,
        })
        file.close()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='test post edited').exists())
    
    def test_compare_post(self):
        response = self.client.post(reverse('compare'), {
            'post1':self.test_post1.pk,
            'post2':self.test_post2.pk,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/compare.html')
    
    def test_create_post_invalid(self):
        response = self.client.post(reverse('create_post'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(Post.objects.all()), 2)
        self.assertTemplateUsed(response, 'post/create_post.html')

    def test_edit_post_invalid(self):
        response = self.client.post(reverse('edit_post', kwargs={'post_id':self.test_post1.pk}), {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/edit_post.html')

    def test_compare_null(self):
        response = self.client.post(reverse('compare'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/compare.html')

    def test_delete_not_self(self):
        temp_user = User.objects.create_user(username='tempuser', password='temppass')
        temp_client = Client()
        temp_client.login(username='tempuser', password='temppass')
        response = temp_client.post(reverse('delete', kwargs={'post_id':self.test_post1.pk}))
        self.assertTrue(response.status_code, 302)
        self.assertTemplateUsed('main/home.html')

    def test_edit_post_not_self(self):
        temp_user = User.objects.create_user(username='tempuser', password='temppass')
        temp_client = Client()
        temp_client.login(username='tempuser', password='temppass')
        response = temp_client.post(reverse('edit_post', kwargs={'post_id':self.test_post1.pk}), {})
        self.assertTrue(response.status_code, 302)
        self.assertTemplateUsed('main/home.html')

    def test_view_post_404(self):
        response = self.client.get(reverse('view_post', kwargs={'post_id':'101'}))
        self.assertEqual(response.status_code, 404)
    
    def test_edit_post_404(self):
        response = self.client.post(reverse('edit_post', kwargs={'post_id':'12'}))
        self.assertTrue(response.status_code, 404)

    def test_compare_404(self):
        response = self.client.post(reverse('compare'), {
            'post1': '101',
            'post2': '102',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('post/compare.html')
        
    def test_delete_404(self):
        response = self.client.post(reverse('delete', kwargs={'post_id':'12'}))
        self.assertTrue(response.status_code, 302)
        self.assertTemplateUsed('main/home.html')