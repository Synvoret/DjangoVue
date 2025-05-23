import graphene
import graphql_jwt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from profiles.models import Profile

from .types import AuthorType, UserType


# PROFILEs
class CreateProfile(graphene.Mutation):
    user = graphene.Field(AuthorType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String()
        website = graphene.String()
        bio = graphene.String()

    def mutate(self, info, username, password, email=None, website=None, bio=None):
        if User.objects.filter(username=username).exists():
            raise Exception("Username already taken.")
        if User.objects.filter(email=email).exists():
            raise Exception("Email already taken.")
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        profile = Profile.objects.create(user=user, website=website, bio=bio)
        return CreateProfile(user=profile)


class DeleteUser(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise Exception("Invalid credentials")
        try:
            profile = Profile.objects.get(user=user)
            profile.delete()
        except Profile.DoesNotExist:
            pass
        user.delete()

        return DeleteUser(success=True)


class LoginUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise Exception("Invalid credentials.")
        login(info.context, user)  # login user and session open

        return LoginUser(user=user)


class LogoutUser(graphene.Mutation):
    success = graphene.Boolean()

    def mutate(self, info):
        request = info.context
        logout(request)
        return LogoutUser(success=True)


class Mutation(graphene.ObjectType):
    # JWT
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    # PROFILEs (create & login)
    create_profile = CreateProfile.Field()
    delete_user = DeleteUser.Field()
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()


schema = graphene.Schema(mutation=Mutation)
