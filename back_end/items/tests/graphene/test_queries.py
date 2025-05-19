import json

from graphene_django.utils.testing import GraphQLTestCase

from django.contrib.auth import get_user_model
from items.models import Item
from profiles.models import Profile
from backend.schema import schema


class ItemsQueriesTests(GraphQLTestCase):
    """Test cases for GraphQL queries related to items."""
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = "/graphql/"

    def setUp(self):
        self.author1 = Profile.objects.create(
            user=get_user_model().objects.create_user(
                username="testuser1",
                email="testuser1@testuser1.com",
                password="testpass1",
            )
        )
        self.author2 = Profile.objects.create(
            user=get_user_model().objects.create_user(
                username="testuser2",
                email="testuser2@testuser2.com",
                password="testpass2",
            )
        )
        Item.objects.create(
            name="Test item 1",
            description="Test description 1",
            author=self.author1,
            created_at="2023-10-01T12:00:00Z",
        )
        Item.objects.create(
            name="Test item 2",
            description="Test description 2",
            author=self.author2,
            created_at="2023-10-02T12:00:00Z",
        )

    def test_items_query(self):
        """Test the items query."""
        response = self.query(
            """
            query {
                items {
                    id
                    name
                    description
                    author {
                        user {
                            username
                            email
                        }
                    }
                }
            }
            """
        )

        content = response.json()
        self.assertResponseNoErrors(response)
        self.assertEqual(len(content["data"]["items"]), 2)
        self.assertEqual(content["data"]["items"][0]["name"], "Test item 1")
        self.assertEqual(
            content["data"]["items"][0]["description"], "Test description 1"
        )
        self.assertEqual(
            content["data"]["items"][0]["author"]["user"]["username"], "testuser1"
        )
