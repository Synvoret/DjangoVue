import graphene
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate
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

    def resolve_all_posts(root, info):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .all()
        )
    
    def resolve_author_by_username(root, info, username):
        return models.Profile.objects.select_related("user").get(user__username=username)
    
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
    
    # CRUD
    def resolve_items(self, info, **kwargs):
        return models.Item.objects.all()
    
    # PROFILEs
    def resolve_profiles(self, info):
        return models.Profile.objects.all()


# CRUD
class CreateItem(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
    
    item = graphene.Field(ItemType)

    def mutate(self, info, name, description):
        item = models.Item(name=name, description=description)
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
    profile = graphene.Field(AuthorType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        website = graphene.String()
        bio = graphene.String()
    
    def mutate(self, info, username, password, website=None, bio=None):
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
        profile = models.Profile(user=user, website=website, bio=bio)
        profile.save()
        return CreateProfile(profile=profile)


class LoginProfile(graphene.Mutation):
    profile = graphene.Field(AuthorType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise Exception('Invalid credentials.')
        profile = models.Profile.objects.get(user=user)
        return LoginProfile(profile=profile)


class Mutation(graphene.ObjectType):
    # CRUD
    create_item = CreateItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()
    # PROFILEs
    create_profile = CreateProfile.Field()
    login_profile = LoginProfile.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
