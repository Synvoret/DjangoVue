import graphene
from django.contrib.auth import get_user_model

from blog import models

from .types import AuthorType, PostType, UserType


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    author_by_username = graphene.Field(AuthorType, username=graphene.String())
    post_by_slug = graphene.Field(PostType, slug=graphene.String())
    posts_by_author = graphene.List(PostType, username=graphene.String())
    posts_by_tag = graphene.List(PostType, tag=graphene.String())
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
            return user

        return None


schema = graphene.Schema(query=Query)
