import graphene

from blog.models import Profile
from items.models import Item

from .types import ItemType


# CRUD
class CreateItem(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    item = graphene.Field(ItemType)

    def mutate(self, info, name, description=None):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication required to create new item.")
        profile = Profile.objects.get(user=user)
        item = Item(name=name, description=description, author=profile)
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
            item = Item.objects.get(pk=id)
        except Item.DoesNotExist:
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
            item = Item.objects.get(pk=id)
            item.delete()
            return DeleteItem(success=True)
        except Item.DoesNotExist:
            raise Exception("Item not found.")
        except Exception as e:
            raise Exception(f"Error occured: {str(e)}.")


class Mutation(graphene.ObjectType):
    # CRUD
    create_item = CreateItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()


schema = graphene.Schema(mutation=Mutation)
