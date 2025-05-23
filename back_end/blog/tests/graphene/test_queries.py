import json

from django.contrib.auth import get_user_model
from graphene_django.utils.testing import GraphQLTestCase

from backend.schema import schema
from blog.models import Post, Tag
from profiles.models import Profile


class BlogQueryTestCase(GraphQLTestCase):
    """Test cases for GraphQL queries related to blog posts."""

    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = "/graphql/"

    def setUp(self):
        """Set up test data."""
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.profile = Profile.objects.create(user=self.user, bio="Test bio")
        self.post1 = Post.objects.create(
            title="Test post 1",
            slug="test-post-1",
            body="Test body 1",
            author=self.profile,
        )
        self.post2 = Post.objects.create(
            title="Test post 2",
            slug="test-post-2",
            body="Test body 2",
            author=self.profile,
        )
        self.tag = Tag.objects.create(name="Test tag")
        self.post1.tags.add(self.tag)
        self.post2.tags.add(self.tag)

    def test_all_posts_query(self):
        """Test querying all posts."""
        response = self.query(
            """
            query {
                allPosts {
                    title
                    slug
                    author {
                        user {
                            username
                        }
                    }
                    tags {
                        name
                    }
                }
            }
            """
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        data = content["data"]["allPosts"]
        self.assertEqual(len(data), 2)

    def test_post_by_slug_query(self):
        """Test querying a post by slug."""
        response = self.query(
            """
            query {
                postBySlug(slug: "test-post-1") {
                    title
                    slug
                }
            }
            """
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content["data"]["postBySlug"]["slug"], "test-post-1")

    def test_author_by_username_query(self):
        """Test querying an author by username."""
        response = self.query(
            """
            query {
                authorByUsername(username: "testuser") {
                    user {
                        username
                    }
                    bio
                }
            }
            """
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(
            content["data"]["authorByUsername"]["user"]["username"], "testuser"
        )

    def test_posts_by_author_query(self):
        """Test querying posts by author username."""
        response = self.query(
            """
            query {
                postsByAuthor(username: "testuser") {
                    title
                    slug
                }
            }
            """
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(len(content["data"]["postsByAuthor"]), 2)

    def test_posts_by_tag_query(self):
        """Test querying posts by tag."""
        response = self.query(
            """
            query {
                postsByTag(tag: "Test tag") {
                    title
                    tags {
                        name
                    }
                }
            }
            """
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        posts = content["data"]["postsByTag"]
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0]["tags"][0]["name"], "Test tag")
