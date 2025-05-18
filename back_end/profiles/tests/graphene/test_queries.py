from django.contrib.auth import get_user_model
from graphene_django.utils.testing import GraphQLTestCase

from profiles.models import Profile
from backend.schema import schema  # zamień 'yourapp' na nazwę twojej aplikacji


class QueryTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema  # ustawiamy nasze schema

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.profile = Profile.objects.create(user=self.user, bio="Bio test")

    def test_profiles_query(self):
        response = self.query(
            '''
            query {
                profiles {
                    id
                    bio
                    user {
                        username
                    }
                }
            }
            ''',
            op_name='profiles',
            variables={'id': 1, 'bio': 'xxx'}
        )

        content = response.json()
        self.assertResponseNoErrors(response)
        self.assertEqual(content["data"]["profiles"][0]["user"]["username"], "testuser")

    def test_users_query(self):
        response = self.query(
            '''
            query {
                users {
                    username
                    email
                }
            }
            '''
        )
        content = response.json()
        self.assertResponseNoErrors(response)
        self.assertEqual(content["data"]["users"][0]["username"], "testuser")

    def test_check_auth_not_authenticated(self):
        response = self.query(
            '''
            query {
                checkAuth {
                    username
                    email
                }
            }
            '''
        )
        content = response.json()
        self.assertIsNone(content["data"]["checkAuth"])

    def test_check_auth_authenticated(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.query(
            '''
            query {
                checkAuth {
                    username
                    email
                }
            }
            '''
        )
        content = response.json()
        self.assertResponseNoErrors(response)
        self.assertEqual(content["data"]["checkAuth"]["username"], "testuser")
