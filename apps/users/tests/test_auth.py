from django.urls import reverse
from rest_framework.test import APITestCase

from apps.users.models import User, UserRole


class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            role=UserRole.ADMIN,
        )

    def test_login_and_me(self):
        # login
        res = self.client.post("/api/auth/login/", {"email": "test@example.com", "password": "testpass123"}, format="json")
        self.assertEqual(res.status_code, 200)

        # me
        res = self.client.get("/api/auth/me/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["email"], "test@example.com")
        self.assertEqual(res.data["role"], UserRole.ADMIN)
