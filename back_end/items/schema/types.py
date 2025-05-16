from graphene_django import DjangoObjectType

from items.models import Item


# CRUD
class ItemType(DjangoObjectType):
    class Meta:
        model = Item
        fields = "__all__"
