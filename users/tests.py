from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

from .models import Profile
from .views import register, profile


class SimpleTest(TestCase):
    user: User

    def create_user(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='morty', email='morty@bloggable.com', password='top_secret')
        return self.user