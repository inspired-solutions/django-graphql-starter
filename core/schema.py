import graphene

from core.schemas.group import Query as GroupQuery, Mutation as GroupMutation
from core.schemas.user import Query as UserQuery


class Query(
        GroupQuery,
        UserQuery,
        graphene.ObjectType):
    pass


class Mutation(
        GroupMutation,
        graphene.ObjectType):
    pass
