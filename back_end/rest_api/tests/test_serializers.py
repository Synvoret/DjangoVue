from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from rest_api.serializers import UserSerializer


class UserSerializerTest(APITestCase):
    def test_user_serialization(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@testuser.com",
            first_name="Test",
            last_name="User",
        )
        serializer = UserSerializer(user)
        data = serializer.data
        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "testuser@testuser.com")

    def test_user_deserialization_valid_data(self):
        data = {
            "username": "testuser",
            "email": "testuser@testuser.com",
            "first_name": "Test",
            "last_name": "User",
            "is_staff": False,
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_user_deserialization_invalid_data(self):
        data = {
            "email": "testuser@testuser.com",
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)
