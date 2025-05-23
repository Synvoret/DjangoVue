import json

from django.contrib.auth.models import User
from django.test import Client
from graphene_django.utils.testing import GraphQLTestCase

from backend.schema import schema


class ProfileMutationsTests(GraphQLTestCase):
    """Test cases for GraphQL mutations related to profiles."""

    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = "/graphql/"

    def setUp(self):
        self.client = Client()
        self.user_data = {
            "username": "testuser",
            "password": "testpass",
            "email": "testuser@testuser.com",
            "website": "user.com",
            "bio": "Test bio",
        }

    def test_create_profile_mutation(self):
        response = self.query(
            """
            mutation CreateProfile($username: String!, $password: String!, $website: String, $bio: String) {
                createProfile(username: $username, password: $password, website: $website, bio: $bio) {
                    user {
                        user {
                            username
                            password
                        }
                        website
                        bio
                    }
                }
            }
            """,
            variables={
                "username": self.user_data["username"],
                "password": self.user_data["password"],
                "website": self.user_data["website"],
                "bio": self.user_data["bio"],
            },
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(
            content["data"]["createProfile"]["user"]["user"]["username"],
            self.user_data["username"],
        )
        self.assertTrue(
            content["data"]["createProfile"]["user"]["user"]["password"] is not None
        )
        self.assertEqual(
            content["data"]["createProfile"]["user"]["website"],
            self.user_data["website"],
        )
        self.assertEqual(
            content["data"]["createProfile"]["user"]["bio"], self.user_data["bio"]
        )
        self.assertTrue(
            User.objects.filter(username=self.user_data["username"]).exists()
        )

    def test_delete_user_mutation(self):
        # create profile
        self.query(
            """
            mutation CreateProfile($username: String!, $password: String!, $website: String, $bio: String) {
                createProfile(username: $username, password: $password, website: $website, bio: $bio) {
                    user {
                        user {
                            username
                            password
                        }
                        website
                        bio
                    }
                }
            }
            """,
            variables={
                "username": self.user_data["username"],
                "password": self.user_data["password"],
                "website": self.user_data["website"],
                "bio": self.user_data["bio"],
            },
        )
        # delete profile
        response = self.query(
            """
            mutation DeleteUser($username: String!, $password: String!) {
                deleteUser(username: $username, password: $password) {
                    success
                }
            }
            """,
            variables={
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content["data"]["deleteUser"]["success"])
        self.assertFalse(
            User.objects.filter(username=self.user_data["username"]).exists()
        )

    def test_login_user_mutation(self):
        User.objects.create_user(
            username=self.user_data["username"], password=self.user_data["password"]
        )
        response = self.query(
            """
            mutation LoginUser($username: String!, $password: String!) {
                loginUser(username: $username, password: $password) {
                    user {
                        username
                        password
                    }
                }
            }
            """,
            variables={
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(
            content["data"]["loginUser"]["user"]["username"], self.user_data["username"]
        )
        self.assertTrue(content["data"]["loginUser"]["user"]["password"] is not None)
        self.assertTrue(
            User.objects.filter(username=self.user_data["username"]).exists()
        )

    def test_login_user_invalid_credentials_mutation(self):
        response = self.query(
            """
            mutation {
                loginUser(username: "wrong user", password: "wrong password") {
                    user {
                        username
                    }
                }
            }
            """
        )
        content = json.loads(response.content)
        self.assertIn("errors", content)
        self.assertResponseHasErrors(response)
        self.assertEqual(content["errors"][0]["message"], "Invalid credentials.")

    def test_logout_user_mutation(self):
        self.client.login(
            username=self.user_data["username"], password=self.user_data["password"]
        )
        response = self.query(
            """
            mutation {
                logoutUser {
                    success
                }
            }
            """
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content["data"]["logoutUser"]["success"])
