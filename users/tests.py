from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.test import Client
from django.urls import reverse

from .models import Profile
from .views import register, profile


class ProfileTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_create_user(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='morty', email='morty@bloggable.com', password='top_secret')
        # Profile.objects.create(user=self.user, bio="profile tester")
        # profile = Profile.objects.get(pk=1)
        self.assertEqual(str(self.user.profile), 'morty Profile')

    def test_register_page(self):
        request = self.factory.get('/register')
        response = register(request)
        self.assertEqual(response.status_code, 200)

    def test_profile_page(self):
        request = self.factory.get('/profile')
        request.user = self.user
        response = profile(request)
        self.assertEqual(response.status_code, 200)
