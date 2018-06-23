import graphene

from core.schema import Query as ApiQuery, Mutation as ApiMutation


class Query(
            ApiQuery,
            graphene.ObjectType):
    """
    Query
    """
    pass


class Mutation(
            ApiMutation,
            graphene.ObjectType):
    """
    Mutation
    """
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
