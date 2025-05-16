from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from profiles.models import Profile


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class AuthorType(DjangoObjectType):
    class Meta:
        model = Profile
