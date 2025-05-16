from django.contrib.auth import get_user_model
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
