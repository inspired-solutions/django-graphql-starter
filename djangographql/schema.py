import graphene
from graphene import Node
from graphene_django.debug import DjangoDebug

from core.schema import Query as CoreQuery, Mutation as CoreMutation


class Query(
        CoreQuery,
        graphene.ObjectType):
    """
    Query
    """
    node = Node.Field()
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(
        CoreMutation,
        graphene.ObjectType):
    """
    Mutation
    """
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
