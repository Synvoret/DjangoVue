import graphene
import graphql_jwt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone

from blog import models
from .types import PostType, AuthorType, UserType, ItemType


# CRUD (posts)
class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        subtitle = graphene.String()
        slug = graphene.String(required=True)
        body = graphene.String(required=True)
        meta_description = graphene.String()
        publish_date = graphene.DateTime()
        tags = graphene.List(graphene.String)

    post = graphene.Field(PostType)

    def mutate(
        self,
        info,
        title,
        slug,
        body,
        subtitle="",
        meta_description="",
        publish_date=None,
        tags=None,
    ):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication required to create new post.")

        profile = models.Profile.objects.get(user=user)
        if not publish_date:
            publish_date = timezone.now()
        post = models.Post(
            title=title,
            subtitle=subtitle,
            slug=slug,
            body=body,
            meta_description=meta_description,
            publish_date=publish_date,
            author=profile,
        )
        post.save()

        if tags:
            for tag in tags:
                tag_instance, created = models.Tag.objects.get_or_create(name=tag)
                post.tags.add(tag_instance)

        post.save()
        return CreatePost(post=post)


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
    # CRUD (posts)
    create_post = CreatePost.Field()
    # CRUD
    create_item = CreateItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()
    # PROFILEs (create & login)
    create_profile = CreateProfile.Field()
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()


schema = graphene.Schema(mutation=Mutation)
