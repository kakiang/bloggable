from django.test import TestCase

from django.urls import reverse
from .models import Post


class PostModelTests(TestCase):
    @staticmethod
    def create_post(title, author):
        """
        Create a post with the given 'title' and by the given 'author'
        """
        return Post.objects.create(title=title)

#     def test_was_published_recently_with_recent_question(self):
#         """
#         was_published_recently() returns True for questions whose pub_date
#         is within the last day.
#         """
#         time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
#         recent_question = Question(pub_date=time)
#         self.assertIs(recent_question.was_published_recently(), True)

    
#     def test_future_question(self):
#         """
#         Questions with a pub_date in the future aren't displayed on
#         the index page.
#         """
#         create_question(question_text='Future question.', days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertContains(response, "No polls are available")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
#     def test_future_question_and_past_question(self):
#         """
#         Even if both past and future questions exist, only past questions
#         are displayed.
#         """
#         create_question(question_text='Past question.', days=-30)
#         create_question(question_text='Future question.', days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'], 
#             ['<Question: Past question.>']
#         )
