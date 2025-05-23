import json

from django.contrib.auth import get_user_model
from django.utils import timezone
from graphene_django.utils.testing import GraphQLTestCase

from profiles.models import Profile


class CreatePostTestCase(GraphQLTestCase):
    """Test cases for the CreatePost mutation."""

    GRAPHQL_SCHEMA = "backend.schema.schema"
    GRAPHQL_URL = "/graphql/"

    def setUp(self):
        """Set up test data."""
        self.user = get_user_model().objects.create_user(
            username="testuser", email="testuser@testuser.com", password="testpass"
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_create_post_mutation(self):
        """Test creating a post using the CreatePost mutation."""
        self.client.force_login(self.user)

        response = self.query(
            """
            mutation CreatePost(
                $title: String!,
                $slug: String!,
                $body: String!,
                $subtitle: String,
                $metaDescription: String,
                $publishDate: DateTime,
                $tags: [String]
            ) {
                createPost(
                    title: $title,
                    slug: $slug,
                    body: $body,
                    subtitle: $subtitle,
                    metaDescription: $metaDescription,
                    publishDate: $publishDate,
                    tags: $tags
                ) {
                    post {
                        title
                        slug
                        body
                        subtitle
                        metaDescription
                        publishDate
                        tags {
                            name
                        }
                        author {
                            user {
                                username
                            }
                        }
                    }
                }
            }
            """,
            variables={
                "title": "Test post",
                "slug": "test-post",
                "body": "Test body",
                "subtitle": "Test subtitle",
                "metaDescription": "Test meta description",
                "publishDate": timezone.now().isoformat(),
                "tags": ["Tag1", "Tag2"],
            },
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

        post_data = content["data"]["createPost"]["post"]
        self.assertEqual(post_data["title"], "Test post")
        self.assertEqual(post_data["slug"], "test-post")
        self.assertEqual(post_data["body"], "Test body")
        self.assertEqual(post_data["subtitle"], "Test subtitle")
        self.assertEqual(post_data["metaDescription"], "Test meta description")
        self.assertEqual(post_data["author"]["user"]["username"], "testuser")
        self.assertIn({"name": "Tag1"}, post_data["tags"])
        self.assertIn({"name": "Tag2"}, post_data["tags"])
