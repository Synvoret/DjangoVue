import graphene

import blog.schema
import items.schema


class Query(blog.schema.BlogQuery, items.schema.ItemsQuery, graphene.ObjectType):
    pass


class Mutation(
    blog.schema.BlogMutation, items.schema.ItemsMutation, graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
