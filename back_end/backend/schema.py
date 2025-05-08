import graphene
import graphql_jwt
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType

from blog import models


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class AuthorType(DjangoObjectType):
    class Meta:
        model = models.Profile


class PostType(DjangoObjectType):
    class Meta:
        model = models.Post


class TagType(DjangoObjectType):
    class Meta:
        model = models.Tag


# CRUD
class ItemType(DjangoObjectType):
    class Meta:
        model = models.Item
        fields = "__all__"


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    author_by_username = graphene.Field(AuthorType, username=graphene.String())
    post_by_slug = graphene.Field(PostType, slug=graphene.String())
    posts_by_author = graphene.List(PostType, username=graphene.String())
    posts_by_tag = graphene.List(PostType, tag=graphene.String())
    # CRUD
    items = graphene.List(ItemType)
    # PROFILEs
    profiles = graphene.List(AuthorType)
    check_auth = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_all_posts(root, info):
        return (
            models.Post.objects.prefetch_related("tags").select_related("author").all()
        )

    def resolve_author_by_username(root, info, username):
        return models.Profile.objects.select_related("user").get(
            user__username=username
        )

    def resolve_post_by_slug(root, info, slug):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )

    def resolve_posts_by_author(root, info, username):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(author__user__username=username)
        )

    def resolve_posts_by_tag(root, info, tag):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(tags__name__iexact=tag)
        )

    def resolve_users(root, info):
        return get_user_model().objects.all()

    # CRUD
    def resolve_items(self, info, **kwargs):
        return models.Item.objects.all()

    # PROFILEs
    def resolve_profiles(self, info):
        return models.Profile.objects.all()

    def resolve_check_auth(self, info):
        user = info.context.user

        request = info.context
        session_key = request.session.session_key
        is_authenticated = request.user.is_authenticated
        print(f"🔐 SESSION KEY: {session_key}")
        print(f"👤 USER: {request.user}, Authenticated: {is_authenticated}")

        if user.is_authenticated:
            print(user)
            return user

        print(user)
        return None


# CRUD
class CreateItem(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    item = graphene.Field(ItemType)

    def mutate(self, info, name, description=None):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication required to create new item.")
        profile = models.Profile.objects.get(user=user)
        item = models.Item(name=name, description=description, author=profile)
        item.save()
        return CreateItem(item=item)


class UpdateItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()

    item = graphene.Field(ItemType)

    def mutate(self, info, id, name=None, description=None):
        try:
            item = models.Item.objects.get(pk=id)
        except models.Item.DoesNotExist:
            raise Exception("Item not found.")
        if name is not None:
            item.name = name
        if description is not None:
            item.description = description

        item.save()
        return UpdateItem(item=item)


class DeleteItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            item = models.Item.objects.get(pk=id)
            item.delete()
            return DeleteItem(success=True)
        except models.Item.DoesNotExist:
            raise Exception("Item not found.")
        except Exception as e:
            raise Exception(f"Error occured: {str(e)}.")


# PROFILEs
class CreateProfile(graphene.Mutation):
    user = graphene.Field(AuthorType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        website = graphene.String()
        bio = graphene.String()

    def mutate(self, info, username, password, website=None, bio=None):
        if User.objects.filter(username=username).exists():
            raise Exception("Username already taken.")
        user = User.objects.create_user(username=username, password=password)
        profile = models.Profile.objects.create(user=user, website=website, bio=bio)
        return CreateProfile(user=profile)


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
        request = info.context
        session_key = request.session.session_key
        is_authenticated = request.user.is_authenticated

        print(f"🔐 SESSION KEY: {session_key}")
        print(f"👤 USER: {request.user}, Authenticated: {is_authenticated}")
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
    # CRUD
    create_item = CreateItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()
    # PROFILEs (create & login)
    create_profile = CreateProfile.Field()
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
