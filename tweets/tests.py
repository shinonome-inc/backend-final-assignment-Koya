from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from .models import Tweet


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            password="testpassword",
        )
        self.client.login(username="tester", password="testpassword")


class TestHomeView(BaseTestCase):
    def test_success_get(self):
        url = reverse("tweets:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["object_list"], Tweet.objects.all())


class TestTweetCreateView(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("tweets:create")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # 他のテストメソッドも同様に続く


class TestTweetDetailView(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.tweet = Tweet.objects.create(user=self.user, content="testtweet")
        self.url = reverse("tweets:detail", kwargs=dict(pk=self.tweet.pk))

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["tweet"], self.tweet)

    # 他のテストメソッドも同様に続く


class TestTweetDeleteView(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.incorrect_user = User.objects.create_user(
            username="test",
            password="testpassword",
        )
        self.client.login(username="tester", password="testpassword")
        self.tweet = Tweet.objects.create(user=self.user, content="tweet")
        self.ordinary_tweet = Tweet.objects.create(user=self.incorrect_user, content="testtweet")
        self.url = reverse("tweets:delete", kwargs={"pk": self.tweet.pk})
        self.second_url = reverse("tweets:delete", kwargs={"pk": self.ordinary_tweet.pk})
        self.notexsist_url = reverse("tweets:delete", kwargs={"pk": 10000})

    def test_success_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertEqual(Tweet.objects.filter(content="tweet").count(), 0)


class TestLikeView(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.tweet = Tweet.objects.create(user=self.user, content="testtweet")
        self.url = reverse("tweets:like", kwargs=dict(pk=self.tweet.pk))

    def test_success_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["is_liked"], True)
        self.assertEqual(response.json()["total_likes"], 1)


class TestUnLikeView(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.tweet = Tweet.objects.create(user=self.user, content="testtweet")
        self.url = reverse("tweets:unlike", kwargs=dict(pk=self.tweet.pk))

    def test_success_post(self):
        self.client.post(reverse("tweets:like", kwargs=dict(pk=self.tweet.pk)))
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["is_liked"], False)
        self.assertEqual(response.json()["total_likes"], 0)
