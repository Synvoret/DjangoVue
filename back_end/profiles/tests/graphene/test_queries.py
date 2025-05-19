import json

from graphene_django.utils.testing import GraphQLTestCase

from django.contrib.auth import get_user_model
from profiles.models import Profile
from backend.schema import schema

class ProfilesQueriesTests(GraphQLTestCase):
    """Test cases for GraphQL queries related to profiles."""

    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = "/graphql/"

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", email='testuser@testuser.com', password="testpass")
        self.profile = Profile.objects.create(user=self.user, website='user.com', bio="Test bio")

    def test_profiles_query(self):
        response = self.query(
            """
            query {
                profiles {
                    user {
                        username
                        email
                    }
                    website
                    bio
                }
            }
            """
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content["data"]["profiles"][0]["user"]["username"], "testuser")
        self.assertEqual(content["data"]["profiles"][0]["user"]["email"], "testuser@testuser.com")
        self.assertEqual(content["data"]["profiles"][0]["website"], "user.com")
        self.assertEqual(content["data"]["profiles"][0]["bio"], "Test bio")

    def test_users_query(self):
        response = self.query(
            """
            query {
                users {
                    username
                    email
                }
            }
            """
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content["data"]["users"][0]["username"], "testuser")
        self.assertEqual(content["data"]["users"][0]["email"], "testuser@testuser.com")

    def test_check_no_auth_query(self):
        response = self.query(
            """
            query {
                checkAuth {
                    username
                    password
                }
            }
            """
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertIsNone(content["data"]["checkAuth"])

    def test_check_auth_query(self):
        self.client.login(username="testuser", password="testpass")
        response = self.query(
            """
            query {
                checkAuth {
                    username
                    email
                }
            }
            """
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content["data"]["checkAuth"]["username"], "testuser")
