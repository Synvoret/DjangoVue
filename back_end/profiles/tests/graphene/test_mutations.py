from django.test import TestCase, Client
from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token
from profiles.models import Profile
from graphql_jwt.testcases import JSONWebTokenTestCase

from backend.schema import schema  # zamień 'your_app' na faktyczną nazwę Twojej aplikacji


class UserMutationsTests(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.client = Client()
        self.username = "testuser"
        self.password = "securepassword"

    def test_create_profile(self):
        response = self.query(
            '''
            mutation CreateProfile($username: String!, $password: String!, $bio: String) {
                createProfile(username: $username, password: $password, bio: $bio) {
                    user {
                        user {
                            username
                        }
                        bio
                    }
                }
            }
            ''',
            variables={
                "username": self.username,
                "password": self.password,
                "bio": "Test bio"
            }
        )

        content = response.json()
        self.assertResponseNoErrors(response)
        self.assertEqual(content["data"]["createProfile"]["user"]["bio"], "Test bio")
        self.assertTrue(User.objects.filter(username=self.username).exists())

    def test_login_user(self):
        User.objects.create_user(username=self.username, password=self.password)

        response = self.query(
            '''
            mutation LoginUser($username: String!, $password: String!) {
                loginUser(username: $username, password: $password) {
                    user {
                        username
                    }
                }
            }
            ''',
            variables={
                "username": self.username,
                "password": self.password
            }
        )

        content = response.json()
        self.assertResponseNoErrors(response)
        self.assertEqual(content["data"]["loginUser"]["user"]["username"], self.username)

    def test_login_user_invalid_credentials(self):
        response = self.query(
            '''
            mutation {
                loginUser(username: "wrong", password: "wrong") {
                    user {
                        username
                    }
                }
            }
            '''
        )

        self.assertIn("errors", response.json())
        self.assertEqual(response.json()["errors"][0]["message"], "Invalid credentials.")

    def test_logout_user(self):
        user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

        response = self.query(
            '''
            mutation {
                logoutUser {
                    success
                }
            }
            ''',
            headers={"Cookie": self.client.cookies.output(header="", sep="; ")}
        )

        content = response.json()
        self.assertResponseNoErrors(response)
        self.assertTrue(content["data"]["logoutUser"]["success"])


class JWTAuthTests(JSONWebTokenTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jwtuser", password="jwtpass")

    def test_obtain_jwt_token(self):
        response = self.client.execute(
            '''
            mutation TokenAuth($username: String!, $password: String!) {
                tokenAuth(username: $username, password: $password) {
                    token
                }
            }
            ''',
            variables={
                "username": "jwtuser",
                "password": "jwtpass"
            }
        )
        token = response.data["tokenAuth"]["token"]
        self.assertIsNotNone(token)

    def test_verify_jwt_token(self):
        token = get_token(self.user)
        response = self.client.execute(
            '''
            mutation VerifyToken($token: String!) {
                verifyToken(token: $token) {
                    payload
                }
            }
            ''',
            variables={"token": token}
        )
        self.assertIn("payload", response.data["verifyToken"])

    def test_refresh_jwt_token(self):
        from graphql_jwt.shortcuts import get_refresh_token

        refresh_token = get_refresh_token(self.user)
        response = self.client.execute(
            '''
            mutation RefreshToken($token: String!) {
                refreshToken(token: $token) {
                    token
                }
            }
            ''',
            variables={"token": str(refresh_token)}
        )
        self.assertIn("token", response.data["refreshToken"])
