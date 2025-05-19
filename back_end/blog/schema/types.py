from graphene_django import DjangoObjectType

from blog.models import Post, Tag
from profiles.models import Profile


class AuthorType(DjangoObjectType):
    class Meta:
        model = Profile


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
