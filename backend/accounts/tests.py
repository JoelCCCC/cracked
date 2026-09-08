from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_and_login(self):
        # Register
        res = self.client.post("/api/auth/register/", {
            "username": "tester",
            "email": "tester@example.com",
            "password": "Password123!",
            "display_name": "Tester Bot"
        })
        self.assertEqual(res.status_code, 201)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)
        self.assertEqual(res.data["user"]["username"], "tester")
        self.assertEqual(res.data["user"]["rank"], "Script Kiddie")

        token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Me endpoint
        me_res = self.client.get("/api/auth/me/")
        self.assertEqual(me_res.status_code, 200)
        self.assertEqual(me_res.data["username"], "tester")
        self.assertEqual(me_res.data["display_name"], "Tester Bot")
