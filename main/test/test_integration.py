from django.test import TestCase, Client
from django.urls import reverse
from main.models import User, Profile
from post.models import Post, Tag   
from django.db.models import Q
from django.core.files import File

class TestIntegration(TestCase):

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
    '''
    def test_integration1(self):
        response = self.client.post(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('main/home.html')
        
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
        
    def test_integration2(self):
        self.client.logout()
        response = self.client.post(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('registration/login.html')

        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('main/home.html')

    def test_integration3(self):
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

        response = self.client.get(reverse('profile', kwargs={'user_id':self.test_user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile.html')

    def test_integration4(self):
        response = self.client.get(reverse('view_post', kwargs={'post_id':self.test_post1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/view_post.html')

        file = open('test_file/test_article_2.pdf', 'rb')
        response = self.client.post(reverse('edit_post', kwargs={'post_id':self.test_post1.pk}), {
            'title': 'test post edited',
            'description': 'this is a test post edited',
            'file': file,
        })
        file.close()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='test post edited').exists())

    def test_integration5(self):
        response = self.client.get(reverse('profile', kwargs={'user_id':self.test_user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile.html')

        response = self.client.post(reverse('profile_edit'), {
            'username': 'editeduser',
            'email': 'editedemail@edited.com',
            'work_at': 'test work place',
            'intro': 'test intro',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Profile.objects.filter(user__username='editeduser').exists())
        self.assertTemplateUsed('main/profile.html')

    def test_integration6(self):
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

        post = Post.objects.get(title='new_article')
        response = self.client.get(reverse('view_post', kwargs={'post_id':post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/view_post.html')

    def test_itegration7(self):
        file = open('test_file/test_article_2.pdf', 'rb')
        response = self.client.post(reverse('edit_post', kwargs={'post_id':self.test_post1.pk}), {
            'title': 'test post edited',
            'description': 'this is a test post edited',
            'file': file,
        })
        file.close()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='test post edited').exists())
        
        response = self.client.post(reverse('compare'), {
            'post1':self.test_post1.pk,
            'post2':self.test_post2.pk,
        })
        self.assertEqual(response.status_code, 200)

    def test_integration8(self):
        response = self.client.get(reverse('delete', kwargs={'post_id':self.test_post1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('main/profile.html')
        self.assertFalse(Post.objects.filter(id=self.test_post1.pk).exists())

        response = self.client.post(reverse('search'), {
            'searched': 'post1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(title__contains='post1').exists())

    def test_integration9(self):
        response = self.client.post(reverse('profile_edit'), {
            'username': 'editeduser',
            'email': 'editedemail@edited.com',
            'work_at': 'test work place',
            'intro': 'test intro',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Profile.objects.filter(user__username='editeduser').exists())
        self.assertTemplateUsed('main/profile.html')

        response = self.client.post(reverse('search'), {
            'searched': 'editeduser'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(Post.objects.filter(author__username__contains='editeduser')), 2)

    def test_itegration10(self):
        response = self.client.get(reverse('profile', kwargs={'user_id':self.test_user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile.html')
        
        response = self.client.get(reverse('delete', kwargs={'post_id':self.test_post1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('main/profile.html')
        self.assertFalse(Post.objects.filter(id=self.test_post1.pk).exists())

        response = self.client.post(reverse('search'), {
            'searched': 'testuser'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(Post.objects.filter(author__username__contains='testuser')), 1)

    def test_itegration11(self):
        response = self.client.get(reverse('profile', kwargs={'user_id':self.test_user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile.html')
        
        response = self.client.get(reverse('delete', kwargs={'post_id':self.test_post1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('main/profile.html')
        self.assertFalse(Post.objects.filter(id=self.test_post1.pk).exists())

        response = self.client.get(reverse('view_post', kwargs={'post_id':self.test_post1.pk}))
        self.assertEqual(response.status_code, 404)

    def test_integration12(self):
        response = self.client.post(reverse('search'), {
            'searched': 'testuser'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(Post.objects.filter(author__username__contains='testuser')), 2)

        response = self.client.get(reverse('profile', kwargs={'user_id':self.test_user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile.html')

        response = self.client.get(reverse('view_post', kwargs={'post_id':self.test_post1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/view_post.html')

    def test_itegration13(self):
        response = self.client.post(reverse('compare'), {
            'post1':self.test_post1.pk,
            'post2':self.test_post2.pk,
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('view_post', kwargs={'post_id':self.test_post1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/view_post.html')

        self.client.logout()
        response = self.client.post(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('registration/login.html')

    def test_itegration14(self):
        response = self.client.post(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('main/home.html')

        self.client.logout()
        response = self.client.post(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('registration/login.html')

        response = self.client.post(reverse('signup'), {
            'username': 'testuser2',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Profile.objects.filter(user__username='testuser2').exists())
        self.assertTemplateUsed('main/home.html')
    '''
    def test_integration15(self):
        self.client.logout()
        response = self.client.post(reverse('signup'), {
            'username': 'testuser2',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Profile.objects.filter(user__username='testuser2').exists())
        self.assertTemplateUsed('main/home.html')

        response = self.client.post(reverse('search'), {
            'searched': 'testuser2'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(author__username__contains='testuser2').exists())

        user = User.objects.get(username='testuser2')
        response = self.client.get(reverse('profile', kwargs={'user_id':user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile.html')