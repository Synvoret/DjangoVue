import graphene
from django.contrib.auth import get_user_model

from profiles.models import Profile

from .types import AuthorType, UserType


class Query(graphene.ObjectType):
    # PROFILEs
    profiles = graphene.List(AuthorType)
    my_user = graphene.Field(UserType)
    check_auth = graphene.Field(UserType)
    users = graphene.List(UserType)

    # PROFILEs
    def resolve_profiles(self, info):
        return Profile.objects.all()

    def resolve_my_user(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None

    def resolve_users(root, info):
        return get_user_model().objects.all()

    def resolve_check_auth(self, info):
        user = info.context.user

        if user.is_authenticated:
            return user

        return None


schema = graphene.Schema(query=Query)
