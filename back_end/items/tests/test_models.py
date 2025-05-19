from django.contrib.auth import get_user_model
from django.test import TestCase
from profiles.models import Profile
from items.models import Item


class ItemModelTests(TestCase):
    """Test cases for the Item model."""
    def setUp(self):
        """Set up test data."""
        self.profile = Profile.objects.create(
            user=get_user_model().objects.create_user(
                username="testuser",
                email="testuser@testuser.com",
                password="testpass",
            )
        )

    def test_item_creation(self):
        """Test creating an item."""
        self.item = Item.objects.create(
            name="Test item", description="Test description", author=self.profile
        )
        self.assertEqual(self.item.name, "Test item")
        self.assertEqual(self.item.description, "Test description")
        self.assertEqual(self.item.author, self.profile)
        self.assertIsNotNone(self.item.created_at)
