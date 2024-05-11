from django.test import SimpleTestCase
from django.urls import resolve, reverse
from post.views import create_post, edit_post, view_post, delete, compare

class TestUrl(SimpleTestCase):
    '''
    def test_create_post_url(self):
        url = reverse('create_post')
        print(resolve(url))
        self.assertEqual(resolve(url).func, create_post)

    def test_edit_post_url(self):
        url = reverse('edit_post', kwargs={'post_id':'1'})
        print(resolve(url))
        self.assertEqual(resolve(url).func, edit_post)

    def test_view_post_url(self):
        url = reverse('view_post', kwargs={'post_id':'1'})
        print(resolve(url))
        self.assertEqual(resolve(url).func, view_post)

    def test_delete_url(self):
        url = reverse('delete', kwargs={'post_id':'1'})
        print(resolve(url))
        self.assertEqual(resolve(url).func, delete)

    def test_compare_url(self):
        url = reverse('compare')
        print(resolve(url))
        self.assertEqual(resolve(url).func, compare)
    '''