import graphene

import blog.schema


class Query(blog.schema.BlogQuery, graphene.ObjectType):
    pass


class Mutation(blog.schema.BlogMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
