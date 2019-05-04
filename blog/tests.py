from django.test import TestCase

from django.urls import reverse
from .models import Post


class PostModelTests(TestCase):
    # @staticmethod
    # def test_create_post(self):
    #     """
    #     Create a post with the given 'title' and by the given 'author'
    #     """
    #     return Post.objects.create('title')
    def test_home_page(self):
        response = self.client.get('', HTTP_HOST='http://localhost:8000')
        self.assertEqual(response.status_code, 200)
