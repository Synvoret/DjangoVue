from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username="testuser1",
            email="testuser1@testuser1.com",
            password="password123",
        )
        User.objects.create_user(
            username="testuser2",
            email="testuser2@testuser2.com",
            password="password123",
        )

    def test_user_list(self):
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["username"], "testuser1")
