from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class TestHomeView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            password="testpassword",
        )
        self.client.login(username="tester", password="testpassword")

    def test_success_get(self):
        url = reverse("tweets:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


# class TestTweetCreateView(TestCase):
#     def test_success_get(self):

#     def test_success_post(self):

#     def test_failure_post_with_empty_content(self):

#     def test_failure_post_with_too_long_content(self):


# class TestTweetDetailView(TestCase):
#     def test_success_get(self):


# class TestTweetDeleteView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_incorrect_user(self):


# class TestLikeView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_liked_tweet(self):


# class TestUnLikeView(TestCase):

#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_unliked_tweet(self):
