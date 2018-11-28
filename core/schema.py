import graphene

from core.schemas.group import Query as GroupQuery, Mutation as GroupMutation
from core.schemas.user import Query as UserQuery, Mutation as UserMutation
from core.schemas.auth import Mutation as AuthMutation


class Query(
        GroupQuery,
        UserQuery,
        graphene.ObjectType):
    pass


class Mutation(
        GroupMutation,
        UserMutation,
        AuthMutation,
        graphene.ObjectType):
    pass
