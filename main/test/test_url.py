from django.test import SimpleTestCase
from django.urls import resolve, reverse
from main.views import home, profile_edit, profile, search, signup 

class TestUrl(SimpleTestCase):
    '''
    def test_home_url(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEqual(resolve(url).func, home)

    def test_search_url(self):
        url = reverse('search')
        print(resolve(url))
        self.assertEqual(resolve(url).func, search)
    
    def test_signup_url(self):
        url = reverse('signup')
        print(resolve(url))
        self.assertEqual(resolve(url).func, signup)

    def test_profile_url(self):
        url = reverse('profile', kwargs={'user_id': '10'})
        print(resolve(url))
        self.assertEqual(resolve(url).func, profile)

    def test_profile_edit_url(self):
        url = reverse('profile_edit')
        print(resolve(url))
        self.assertEqual(resolve(url).func, profile_edit)
    '''