from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User

# from django.urls import reverse
from .models import Post, Comment


class PostModelTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='rick', email='rickblog@gmail.com', password='top_secret')
        author = self.user
        Post.objects.create(title='title of post1', author=author)
        Post.objects.create(title='title of post2', author=author)
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_post_slug(self):
        post1 = Post.objects.get(title='title of post1')
        post2 = Post.objects.get(title='title of post2')
        self.assertEqual(post1.slug, 'title-of-post1')
        self.assertEqual(post2.slug, 'title-of-post2')

    def test_comment(self):
        post1 = Post.objects.get(title='title of post1')
        Comment.objects.create(content="first comment to post1", post=post1, author=self.user)
        Comment.objects.create(content="second comment to post1", post=post1, author=self.user)
        self.assertEqual(post1.comment_set.count(), 2)
        comment = Comment.objects.get(pk=1)
        comment.delete()
        self.assertEqual(post1.comment_set.count(), 1)
