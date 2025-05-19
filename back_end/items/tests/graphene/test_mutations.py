import json
from django.contrib.auth import get_user_model
from graphene_django.utils.testing import GraphQLTestCase

from profiles.models import Profile
from items.models import Item
from backend.schema import schema


class ItemMutationsTests(GraphQLTestCase):
    """Test cases for GraphQL mutations related to items."""

    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = "/graphql/"

    def setUp(self):
        """Set up test data."""
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
        self.item_data = {
            "name": "Test item",
            "description": "Test description",
            "author": self.author1,
        }

    def _authenticate(self, author):
        self.client.force_login(author.user)

    def test_create_item_with_auth_mutation(self):
        """Test creating an item with authentication."""
        self._authenticate(self.author1)
        response = self.query(
            """
            mutation CreateItem($name: String!, $description: String) {
                createItem(name: $name, description: $description) {
                    item {
                        id
                        name
                        description
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
                "name": self.item_data["name"],
                "description": self.item_data["description"],
            },
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(
            content["data"]["createItem"]["item"]["name"], self.item_data["name"]
        )
        self.assertEqual(
            content["data"]["createItem"]["item"]["description"],
            self.item_data["description"],
        )
        self.assertEqual(
            content["data"]["createItem"]["item"]["author"]["user"]["username"],
            self.author1.user.username,
        )
        self.assertTrue(Item.objects.filter(name=self.item_data["name"]).exists())
        self.assertTrue(
            Item.objects.filter(description=self.item_data["description"]).exists()
        )
        self.assertTrue(Item.objects.filter(author=self.author1).exists())

    def test_create_item_no_auth_mutation(self):
        """Test creating an item without authentication."""
        response = self.query(
            """
            mutation CreateItem($name: String!, $description: String) {
                createItem(name: $name, description: $description) {
                    item {
                        id
                        name
                        description
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
                "name": self.item_data["name"],
                "description": self.item_data["description"],
            },
        )
        content = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertEqual(
            content["errors"][0]["message"],
            "Authentication required to create new item.",
        )
        self.assertFalse(Item.objects.filter(name=self.item_data["name"]).exists())

    def test_update_item_mutation(self):
        """Test updating an item with authentication."""
        self._authenticate(self.author1)
        item = Item.objects.create(
            name="Test item",
            description="Test description",
            author=self.author1,
        )

        response = self.query(
            """
            mutation UpdateItem($id: ID!, $name: String, $description: String) {
                updateItem(id: $id, name: $name, description: $description) {
                    item {
                        id
                        name
                        description
                    }
                }
            }
            """,
            variables={
                "id": item.id,
                "name": "Updated item",
                "description": "Updated description",
            },
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content["data"]["updateItem"]["item"]["name"], "Updated item")
        self.assertEqual(
            content["data"]["updateItem"]["item"]["description"],
            "Updated description",
        )

    def test_delete_item_mutation(self):
        """Test deleting an item with authentication."""
        self._authenticate(self.author1)
        item = Item.objects.create(
            name="Test item",
            description="Test description",
            author=self.author1,
        )

        response = self.query(
            """
            mutation DeleteItem($id: ID!) {
                deleteItem(id: $id) {
                    success
                }
            }
            """,
            variables={"id": item.id},
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content["data"]["deleteItem"]["success"])
        self.assertFalse(Item.objects.filter(id=item.id).exists())
