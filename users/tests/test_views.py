from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


class UserAuthViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            password="TestPassword123",
            is_active=True,
        )

    def test_home_page_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_logout_view(self):
        self.client.login(email="testuser@example.com", password="TestPassword123")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_login_view_get(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_view_post_valid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {"email": "testuser@example.com", "password": "TestPassword123"},
        )
        self.assertRedirects(response, reverse("home"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_view_post_invalid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {"email": "testuser@example.com", "password": "WrongPassword123"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_register_view_get(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    # def test_register_view_post_valid_data(self):
    #     response = self.client.post(reverse('register'), {
    #         'first_name': 'New',
    #         'last_name': 'User',
    #         'email': 'newuser@example.com',
    #         'password1': 'NewPassword123',
    #         'password2': 'NewPassword123'
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_verify_email_view_valid_link(self):
        user = User.objects.create(
            email="verifyuser@example.com",
            password="VerifyPassword123",
            is_active=False,
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        response = self.client.get(
            reverse("verify_email", kwargs={"uidb64": uid, "token": token})
        )
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertRedirects(response, reverse("login"))

    def test_verify_email_view_invalid_link(self):
        response = self.client.get(
            reverse("verify_email", kwargs={"uidb64": "invalid", "token": "invalid"})
        )
        self.assertRedirects(response, reverse("home"))

    def test_change_password_view_get(self):
        self.client.login(email="testuser@example.com", password="TestPassword123")
        response = self.client.get(reverse("change_password"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/change_password.html")

    def test_change_password_view_post(self):
        self.client.login(email="testuser@example.com", password="TestPassword123")
        response = self.client.post(
            reverse("change_password"),
            {
                "current_password": "TestPassword123",
                "new_password": "NewPassword123",
                "confirm_password": "NewPassword123",
            },
        )
        self.assertRedirects(response, reverse("home"))
        self.client.logout()

        # Test new password login
        login_success = self.client.login(
            email="testuser@example.com", password="NewPassword123"
        )
        self.assertTrue(login_success)
