from tokenize import Token
from rest_framework.test import APISimpleTestCase
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth import get_user_model
from knox.models import AuthToken


class TestUser(APISimpleTestCase):
    databases = ["auth_db"]

    def setUp(self):
        """Clean user table and create admin"""
        # Clean user table
        get_user_model().objects.all().delete()

        self.admin = get_user_model().objects.create_superuser(
            email="admin@admin.com",
            password="admin",
        )

    @staticmethod
    def create_valid_user(username: str, password: str) -> None:
        """Create a valid user"""
        get_user_model().objects.create_user(
            email=username,
            password=password,
        )

    def test_admin_login(self):
        url = reverse("knox_login")
        data = {"username": "admin@admin.com", "password": "admin"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        # Assert that the response contains the token
        self.assertIn("token", response.data)

        # Test login with wrong password
        data = {"username": "admin@admin.com", "password": "wrong"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        # Check if contains non field erros unable to log in...
        self.assertIn(
            "Unable to log in with provided credentials.",
            response.data["non_field_errors"][0],
        )

    def test_admin_logout(self):
        url = reverse("knox_login")
        data = {"username": "admin@admin.com", "password": "admin"}
        response = self.client.post(url, data, format="json")
        token = response.data["token"]
        self.assertEqual(response.status_code, 200)
        # Assert that the response contains the token
        self.assertIn("token", response.data)

        # Logout
        url = reverse("knox_logout")
        headers = {"HTTP_AUTHORIZATION": "Token " + token}
        response = self.client.post(url, **headers, format="json")
        self.assertEqual(response.status_code, 204)

    def test_user_register(self):
        url = reverse("register")
        data = {
            "email": "test@test.com",
            "password1": "123testing123",
            "password2": "123testing123",
            "first_name": "Test",
            "last_name": "User",
            "input_company_name": "Test Company",
            "cellphone": "123456789",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        # Assert that the response DONT contains the token
        self.assertNotIn("token", response.data)

        # Check if CANT login (user should be inactive)
        url = reverse("knox_login")
        data = {"username": "test@test.com", "password": "123testing123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_user_register_activate_login(self):
        """
        Testing the 'almost' complete flow of registering,
        check if inactive, get the token to activate
        and then send it to the activation view.

        This will not be 100% realistic since in reality I would
        need a mail service to send an url with user_id + token to
        the client.

        Also checks if can't activate with invalid token.
        """
        url = reverse("register")
        data = {
            "email": "test@test.com",
            "password1": "123testing123",
            "password2": "123testing123",
            "first_name": "Test",
            "last_name": "User",
            "input_company_name": "Test Company",
            "cellphone": "123456789",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        # Assert that the response DONT contains the token
        self.assertNotIn("token", response.data)

        # Check if CANT login (user should be inactive)
        url = reverse("knox_login")
        data = {"username": "test@test.com", "password": "123testing123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)

        ### THIS PART IS NOT REALISTIC ###
        # 1. Get the user and user_id that was just created
        user = get_user_model().objects.get(email="test@test.com")
        user_id = user.id

        # 2. Generate a new token for the user
        confirmation_token = default_token_generator.make_token(user)

        # 3. Prepare the payload from the data I just got
        payload = {
            "user_id": user_id,
            "token": confirmation_token,
        }

        ### Now its the normal flow of sending to activation view ###
        url = reverse("activate")

        # Before doing it correctly, try to activate with wrong token
        fake_payload = payload.copy()
        fake_payload["token"] = "wrong"
        response = self.client.get(url, fake_payload, format="json")
        self.assertEqual(response.status_code, 403)

        # Try also with corret token but wrong user_id
        fake_payload["token"] = confirmation_token
        fake_payload["user_id"] = "abc123abc"
        response = self.client.get(url, fake_payload, format="json")
        self.assertEqual(response.status_code, 404)

        # Now activate for real
        response = self.client.get(url, payload, format="json")
        self.assertEqual(response.status_code, 200)

        # Check if CAN login (user should be active)
        url = reverse("knox_login")
        data = {"username": "test@test.com", "password": "123testing123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        # Assert that the response contains the token
        self.assertIn("token", response.data)

    def test_multiple_login_and_logout_all(self):
        """
        Create a user, check if can do multiple logins and
        then logout all.
        """
        # Create user
        self.create_valid_user("user@test.com", "123password123")

        # Delete all Tokens from database
        AuthToken.objects.all().delete()

        # Login multiple times
        url = reverse("knox_login")
        data = {"username": "user@test.com", "password": "123password123"}
        token_1 = self.client.post(url, data, format="json").data["token"]
        token_2 = self.client.post(url, data, format="json").data["token"]
        token_3 = self.client.post(url, data, format="json").data["token"]

        # Check if tokens are different
        self.assertNotEqual(token_1, token_2)
        self.assertNotEqual(token_1, token_3)
        self.assertNotEqual(token_2, token_3)

        # Check if there are 3 tokens in the database
        self.assertEqual(AuthToken.objects.count(), 3)

        # Check if can logout all
        url = reverse("knox_logoutall")
        headers = {"HTTP_AUTHORIZATION": "Token " + token_1}
        response = self.client.post(url, **headers, format="json")
        self.assertEqual(response.status_code, 204)

        # Check if there are 0 tokens in the database
        self.assertEqual(AuthToken.objects.count(), 0)


class TestUserPermissions(APISimpleTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="