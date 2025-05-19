from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


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

    def test_list_users(self):
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["username"], "testuser1")

    def test_create_user_valid(self):
        url = reverse("user-list")
        data = {
            "username": "newuser",
            "email": "newuser@newuser.com",
            "first_name": "New",
            "last_name": "User",
            "is_staff": False,
            "date_joined": "2023-10-01T00:00:00Z",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_create_user_missing_username(self):
        url = reverse("user-list")
        data = {"email": "nousername@nousername.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
