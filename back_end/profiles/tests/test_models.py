from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Profile


class ProfileModelTests(TestCase):
    """Test cases for the Profile model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@testuser.com",
            )
        self.profile = Profile.objects.create(
            user=self.user,
            website="user.com",
            bio="Test bio",
        )

    def test_profile_created(self):
        """Test that a profile is created with the correct user."""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.user.email, "testuser@testuser.com")
        self.assertEqual(self.profile.website, "user.com")
        self.assertEqual(self.profile.bio, "Test bio")
    
    def test_profile_str(self):
        """Test the string representation of the profile."""
        self.assertEqual(str(self.profile), 'testuser')
