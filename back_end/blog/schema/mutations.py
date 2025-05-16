import graphene
from django.utils import timezone

from blog.models import Post, Tag
from profiles.models import Profile

from .types import PostType


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

        profile = Profile.objects.get(user=user)
        if not publish_date:
            publish_date = timezone.now()
        post = Post(
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
                tag_instance, created = Tag.objects.get_or_create(name=tag)
                post.tags.add(tag_instance)

        post.save()
        return CreatePost(post=post)


class Mutation(graphene.ObjectType):
    # CRUD (posts)
    create_post = CreatePost.Field()


schema = graphene.Schema(mutation=Mutation)
