from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import Tweet


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


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.url = reverse("tweets:create")
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.force_login(self.user)

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        valid_data = {"username": self.user, "content": "test"}
        response = self.client.post(self.url, valid_data)

        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )

        self.assertTrue(Tweet.objects.filter(id=1).exists())
        tweet = Tweet.objects.get(id=1)
        self.assertEqual(tweet.content, valid_data["content"])

    def test_failure_post_with_empty_content(self):
        invalid_data = {"username": self.user, "content": ""}

        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["content"])
        self.assertFalse(Tweet.objects.filter(id=1).exists())

    def test_failure_post_with_too_long_content(self):
        invalid_data = {
            "username": self.user,
            "content": """
            aaaasaasaaaaaaaaaaasaasaaaaaaaaaaasaasaaaaaaaaaaasaasaaaaaaaaaaasaasaaaaa
            aaaaaasaasaaaaaaaaaaasasaaaaaaaaaaasaasaaaaaaaaaaasaasaaaaaaaaaaasaasaaaaa""",
        }

        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("この値は 140 文字以下でなければなりません( 160 文字になっています)。", form.errors["content"])
        self.assertFalse(Tweet.objects.filter(id=1).exists())


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            password="testpassword",
        )
        self.client.login(username="tester", password="testpassword")
        self.tweet = Tweet.objects.create(user=self.user, content="testtweet")
        self.url = reverse("tweets:detail", kwargs=dict(pk=self.tweet.pk))

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["tweet"], self.tweet)

    class TestTweetDeleteView(TestCase):
        def setUp(self):
            self.user = User.objects.create_user(
                username="tester",
                password="testpassword",
            )
            self.incorrect_user = User.objects.create_user(
                username="test",
                password="testpassword",
            )
            self.client.login(username="tester", password="testpassword")  # 正しいユーザーでログイン
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

        def test_failure_post_with_not_exist_tweet(self):
            response = self.client.post(self.notexsist_url)
            self.assertEqual(response, status_code=404)
            self.assertTrue(Tweet.objects.filter(pk=self.tweet.pk).exists())

        def test_failure_post_with_incorrect_user(self):
            response = self.client.post(self.second_url)
            self.assertEqual(response, status_code=403)
            self.assertTrue(Tweet.objects.filter(pk=self.ordinary_tweet.pk).exists())


# class TestLikeView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_liked_tweet(self):


# class TestUnLikeView(TestCase):

#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_unliked_tweet(self):
