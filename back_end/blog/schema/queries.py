import graphene

from blog.models import Post
from profiles.models import Profile

from .types import AuthorType, PostType


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    author_by_username = graphene.Field(AuthorType, username=graphene.String())
    post_by_slug = graphene.Field(PostType, slug=graphene.String())
    posts_by_author = graphene.List(PostType, username=graphene.String())
    posts_by_tag = graphene.List(PostType, tag=graphene.String())

    def resolve_all_posts(root, info):
        return Post.objects.prefetch_related("tags").select_related("author").all()

    def resolve_author_by_username(root, info, username):
        return Profile.objects.select_related("user").get(user__username=username)

    def resolve_post_by_slug(root, info, slug):
        return (
            Post.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )

    def resolve_posts_by_author(root, info, username):
        return (
            Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(author__user__username=username)
        )

    def resolve_posts_by_tag(root, info, tag):
        return (
            Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(tags__name__iexact=tag)
        )


schema = graphene.Schema(query=Query)
