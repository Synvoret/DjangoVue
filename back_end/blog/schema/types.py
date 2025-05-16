from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from blog.models import Post, Profile, Tag


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class AuthorType(DjangoObjectType):
    class Meta:
        model = Profile


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
