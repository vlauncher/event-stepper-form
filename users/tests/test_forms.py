from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..forms import CustomLoginForm, RegisterForm, ChangePasswordForm

User = get_user_model()


class CustomLoginFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
        )

    def test_valid_login(self):
        form = CustomLoginForm(
            data={"email": "testuser@example.com", "password": "password123"}
        )
        self.assertTrue(form.is_valid())

    def test_invalid_login_wrong_password(self):
        form = CustomLoginForm(
            data={"email": "testuser@example.com", "password": "wrongpassword"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["__all__"], ["Invalid email or password"])

    def test_invalid_login_wrong_email(self):
        form = CustomLoginForm(
            data={"email": "wrong@example.com", "password": "password123"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["__all__"], ["Invalid email or password"])

    def test_get_user(self):
        form = CustomLoginForm(
            data={"email": "testuser@example.com", "password": "password123"}
        )
        form.is_valid()
        user = form.get_user()
        self.assertEqual(user, self.user)


class RegisterFormTest(TestCase):
    def test_valid_registration(self):
        form = RegisterForm(
            data={
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "janedoe@example.com",
                "password": "password123",
                "confirm_password": "password123",
            }
        )
        self.assertTrue(form.is_valid())

    def test_duplicate_email_registration(self):
        User.objects.create_user(
            first_name="Jane",
            last_name="Doe",
            email="existinguser@example.com",
            password="password123",
        )
        form = RegisterForm(
            data={
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "existinguser@example.com",
                "password": "password123",
                "confirm_password": "password123",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["email"], ["A user with this email already exists."]
        )

    def test_password_mismatch(self):
        form = RegisterForm(
            data={
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "janedoe@example.com",
                "password": "password123",
                "confirm_password": "differentpassword",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["__all__"], ["Passwords do not match."])

    def test_save_user(self):
        form = RegisterForm(
            data={
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "janedoe@example.com",
                "password": "password123",
                "confirm_password": "password123",
            }
        )
        if form.is_valid():
            user = form.save()
            self.assertTrue(user.check_password("password123"))
            self.assertEqual(user.email, "janedoe@example.com")


class ChangePasswordFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            password="oldpassword123",
        )

    def test_valid_change_password(self):
        form = ChangePasswordForm(
            data={
                "current_password": "oldpassword123",
                "new_password": "newpassword456",
                "confirm_password": "newpassword456",
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid())

    def test_invalid_current_password(self):
        form = ChangePasswordForm(
            data={
                "current_password": "wrongpassword",
                "new_password": "newpassword456",
                "confirm_password": "newpassword456",
            },
            user=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["current_password"], ["Current password is incorrect."]
        )

    def test_new_password_mismatch(self):
        form = ChangePasswordForm(
            data={
                "current_password": "oldpassword123",
                "new_password": "newpassword456",
                "confirm_password": "differentpassword",
            },
            user=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["__all__"], ["New passwords do not match."])
