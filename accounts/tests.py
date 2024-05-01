from django.conf import settings
from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Friendship
from tweets.models import Tweet

User = get_user_model()


class TestSignupView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_success_post(self):
        valid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, valid_data)

        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )

        self.assertTrue(User.objects.filter(username=valid_data["username"]).exists())
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        invalid_data = {"username": "", "email": "", "password1": "", "password2": ""}
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["username"])
        self.assertIn("このフィールドは必須です。", form.errors["email"])
        self.assertIn("このフィールドは必須です。", form.errors["password1"])
        self.assertIn("このフィールドは必須です。", form.errors["password2"])

    def test_failure_post_with_empty_username(self):
        invalid_data = {
            "username": "",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["username"])

    def test_failure_post_with_empty_email(self):
        invalid_data = {
            "username": "test",
            "email": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["email"])

    def test_failure_post_with_empty_password(self):
        invalid_data = {
            "username": "test",
            "email": "test@test.com",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["password1"])
        self.assertIn("このフィールドは必須です。", form.errors["password2"])

    def test_failure_post_with_duplicated_user(self):
        self.user = User.objects.create_user(
            username="tester",
            password="testpassword",
        )
        invalid_data = {
            "username": "tester",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(
                username=invalid_data["username"], email=invalid_data["email"], password=invalid_data["password1"]
            )
        )
        self.assertFalse(form.is_valid())
        self.assertIn("同じユーザー名が既に登録済みです。", form.errors["username"])

    def test_failure_post_with_invalid_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("有効なメールアドレスを入力してください。", form.errors["email"])

    def test_failure_post_with_too_short_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "pas",
            "password2": "pas",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは短すぎます。最低 8 文字以上必要です。", form.errors["password2"])

    def test_failure_post_with_password_similar_to_username(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testuseri",
            "password2": "testuseri",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは ユーザー名 と似すぎています。", form.errors["password2"])

    def test_failure_post_with_only_numbers_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "123456789",
            "password2": "123456789",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは数字しか使われていません。", form.errors["password2"])

    def test_failure_post_with_mismatch_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpasswor",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("確認用パスワードが一致しません。", form.errors["password2"])


class TestLoginView(TestCase):
    def setUp(self):
        User.objects.create_user(username="test", email="test@test.com", password="testpassword")
        self.url = reverse("accounts:login")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_success_post(self):
        data = {"username": "test", "password": "testpassword"}
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertIn(SESSION_KEY, self.client.session)  # Check if user is logged in

    def test_failure_post_with_not_exists_user(self):
        invalid_data = {"username": "nonexistent", "password": "testpassword"}
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。",
            form.errors["__all__"],
        )
        self.assertNotIn(SESSION_KEY, self.client.session)  # Check if user is logged in

    def test_failure_post_with_empty_password(self):
        invalid_data = {"username": "test", "password": ""}
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertIn("このフィールドは必須です。", form.errors["password"])
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestLogoutView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpasword",
        )

        self.client.login(username="testuser", password="testpssword")

    def test_success_post(self):
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(
            response,
            reverse(settings.LOGOUT_REDIRECT_URL),
            status_code=302,
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProfileView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        self.url = reverse("accounts:user_profile", kwargs={"username": self.user})
        self.tweet = Tweet.objects.create(user=self.user, content="twsttweet")

    def test_success_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")
        self.assertQuerysetEqual(response.context["object_list"], Tweet.objects.all())


# class TestUserProfileEditView(TestCase):
#     def test_success_get(self):

#     def test_success_post(self):

#     def test_failure_post_with_not_exists_user(self):

#     def test_failure_post_with_incorrect_user(self):


class TestFollowView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.user2 = get_user_model().objects.create_user(username="tester", password="testpassword")
        self.client.force_login(self.user)

    def test_success_post(self):
        response = self.client.post(reverse("accounts:follow", kwargs={"username": self.user2.username}))
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(Friendship.objects.filter(follower=self.user, following=self.user2).exists())

    def test_failure_post_with_not_exist_user(self):
        response = self.client.post(reverse("accounts:follow", kwargs={"username": "nonexistent_user"}))
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Friendship.objects.filter(follower=self.user).exists())

    def test_failure_follow_self(self):
        response = self.client.post(reverse("accounts:follow", kwargs={"username": self.user.username}))
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Friendship.objects.filter(follower=self.user, following=self.user).exists())


class TestUnfollowView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.user2 = get_user_model().objects.create_user(username="tester", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        # Add this line to setup a following relationship
        Friendship.objects.create(follower=self.user, following=self.user2)

    def test_success_post(self):
        response = self.client.post(reverse("accounts:unfollow", kwargs={"username": self.user2.username}))
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertFalse(Friendship.objects.filter(follower=self.user, following=self.user2).exists())

    def test_failure_post_with_not_exist_user(self):
        response = self.client.post(reverse("accounts:unfollow", kwargs={"username": "nonexistent_user"}))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Friendship.objects.filter(follower=self.user, following=self.user2).exists())

    def test_failure_post_with_incorrect_user(self):
        user_to_unfollow = get_user_model().objects.create_user(username="user_to_unfollow", password="testpassword")
        response = self.client.post(reverse("accounts:unfollow", kwargs={"username": user_to_unfollow.username}))
        self.assertEqual(response.status_code, 400)
        self.assertTrue(Friendship.objects.filter(follower=self.user, following=self.user2).exists())


class TestFollowingListView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.user2 = get_user_model().objects.create_user(username="tester", password="testpassword")
        self.user3 = get_user_model().objects.create_user(username="tester2", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        self.friendship1 = Friendship.objects.create(follower=self.user, following=self.user2)
        self.friendship2 = Friendship.objects.create(follower=self.user, following=self.user3)

    def test_success_get(self):
        response = self.client.get(reverse("accounts:following_list", kwargs={"username": self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(list(response.context["following_list"]), [self.friendship1, self.friendship2])


class TestFollowerListView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.user2 = get_user_model().objects.create_user(username="tester", password="testpassword")
        self.user3 = get_user_model().objects.create_user(username="tester2", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        Friendship.objects.create(follower=self.user2, following=self.user)
        Friendship.objects.create(follower=self.user3, following=self.user)

    def test_success_get(self):
        response = self.client.get(reverse("accounts:follower_list", kwargs={"username": self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(list(response.context["follower_list"]), Friendship.objects.all())
