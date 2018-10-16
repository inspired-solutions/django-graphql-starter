import graphene
from graphene_django.types import DjangoObjectType

from django.contrib.auth import models as auth_models
from graphene import Node

from opencrud.custom import WithCustomConnection, CustomDjangoFilterConnectionField, CustomDjangoFilterListField, \
    CustomDjangoField


class UserWhereUniqueInput(graphene.InputObjectType):
    id = graphene.ID()


class User(DjangoObjectType):
    @WithCustomConnection(auth_models.User)
    class Meta:
        filter_fields = ('id', 'email', )
        interfaces = (Node, )


class Query(graphene.ObjectType):
    user = CustomDjangoField(User)
    users = CustomDjangoFilterListField(User)
    users_connection = CustomDjangoFilterConnectionField(User)
