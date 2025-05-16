import graphene

import blog.schema
import items.schema
import profiles.schema


class Query(
    blog.schema.BlogQuery,
    items.schema.ItemsQuery,
    profiles.schema.ProfilesQuery,
    graphene.ObjectType,
):
    pass


class Mutation(
    blog.schema.BlogMutation,
    items.schema.ItemsMutation,
    profiles.schema.ProfilesMutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
