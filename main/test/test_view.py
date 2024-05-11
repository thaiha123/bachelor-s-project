from django.test import TestCase, Client
from django.urls import reverse
from main.models import User, Profile
from post.models import Post, Tag   
from main.views import home, profile_edit, profile, search, signup 
from main.forms import signup_form
from django.db.models import Q

class TestViews(TestCase): 
    
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='testpass')
        self.test_profile = Profile.objects.create(user = self.test_user)
        self.test_post = Post.objects.create(author = self.test_user, title='test post', description='This is a test post.')
        self.test_tag = Tag.objects.create(name='test tag')
        self.test_signup_form = signup_form

        self.client = Client()
        self.client.login(username='testuser', password='testpass')

        self.new_client = Client()
    '''
    def test_home_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_signup_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_search_get(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/search.html')

    def test_profile_get(self):
        response = self.client.get(reverse('profile', kwargs={'user_id':self.test_user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile.html')

    def test_profile_edit_get(self):
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile_edit.html')
    
    def test_signup_post(self):
        response = self.new_client.post(reverse('signup'), {
            'username': 'testuser2',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Profile.objects.filter(user__username='testuser2').exists())

    def test_profile_edit_post(self):
        response = self.client.post(reverse('profile_edit'), {
            'username': 'editeduser',
            'email': 'editedemail@edited.com',
            'work_at': 'test work place',
            'intro': 'test intro',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Profile.objects.filter(user__username='editeduser').exists())
        self.assertTemplateUsed('main/profile.html')
    
    def test_search_post(self):
        response = self.client.post(reverse('search'), {
            'searched': 'post'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(Q(title__contains='post') | Q(author__username__contains='post') | Q(tag__name__contains='post')).exists())
    
    def test_signup_invalid(self):
        response = self.new_client.post(reverse('signup'), {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_profile_edit_invalid(self):
        response = self.client.post(reverse('profile_edit'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile_edit.html')

    def test_search_no_res(self):
        response = self.client.post(reverse('search'), {
            'searched': '55555'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(Q(title__contains='55555') | Q(author__username__contains='55555') | Q(tag__name__contains='55555')).exists())
        
    def test_profile_404(self):
        response =  self.client.get(reverse('profile', kwargs={'user_id':'12'}))
        self.assertEqual(response.status_code, 404)
    '''
    