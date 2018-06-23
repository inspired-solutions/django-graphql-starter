import graphene

from core.schema import Query as CoreQuery, Mutation as CoreMutation


class Query(
        CoreQuery,
        graphene.ObjectType):
    """
    Query
    """
    pass


'''class Mutation(
        CoreMutation,
        graphene.ObjectType):
    """
    Mutation
    """
    pass'''


schema = graphene.Schema(query=Query)  # , mutation=Mutation)
