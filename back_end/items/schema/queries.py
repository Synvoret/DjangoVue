import graphene

from items.models import Item

from .types import ItemType


class Query(graphene.ObjectType):
    # CRUD
    items = graphene.List(ItemType)

    # CRUD
    def resolve_items(self, info, **kwargs):
        return Item.objects.all()


schema = graphene.Schema(query=Query)
