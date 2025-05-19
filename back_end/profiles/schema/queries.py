import graphene
from django.contrib.auth import get_user_model

from profiles.models import Profile

from .types import AuthorType, UserType


class Query(graphene.ObjectType):
    # PROFILEs
    profiles = graphene.List(AuthorType)
    check_auth = graphene.Field(UserType)
    users = graphene.List(UserType)

    # PROFILEs
    def resolve_profiles(self, info):
        return Profile.objects.all()

    def resolve_users(root, info):
        return get_user_model().objects.all()

    def resolve_check_auth(self, info):
        user = info.context.user

        # request = info.context
        # session_key = request.session.session_key
        # is_authenticated = request.user.is_authenticated
        # print(f"🔐 SESSION KEY: {session_key}")
        # print(f"👤 USER: {request.user}, Authenticated: {is_authenticated}")

        if user.is_authenticated:
            return user

        return None


schema = graphene.Schema(query=Query)
