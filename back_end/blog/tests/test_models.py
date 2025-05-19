from django.contrib.auth import get_user_model
from django.test import TestCase

from blog.models import Post, Tag
from profiles.models import Profile


class PostModelTests(TestCase):
    """Test cases for the Post model."""

    def setUp(self):
        """Set up test data."""
        self.profile = Profile.objects.create(
            user=get_user_model().objects.create_user(
                username="testuser",
                email="testuser@testuser.com",
                password="testpass",
            )
        )

    def test_post_creation(self):
        """Test creating a post."""
        self.tag = Tag.objects.create(name="Test Tag")
        self.post = Post.objects.create(
            title="Test post",
            subtitle="Test subtitle",
            slug="test-post",
            body="Test body",
            meta_description="Test meta description",
            author=self.profile,
        )
        self.post.tags.add(self.tag)

        self.assertEqual(self.post.title, "Test post")
        self.assertEqual(self.post.subtitle, "Test subtitle")
        self.assertEqual(self.post.slug, "test-post")
        self.assertEqual(self.post.body, "Test body")
        self.assertEqual(self.post.meta_description, "Test meta description")
        self.assertEqual(self.post.author, self.profile)
        self.assertIn(self.tag, self.post.tags.all())
