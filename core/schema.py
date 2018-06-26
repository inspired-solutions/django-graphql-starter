import graphene
# from graphene import Node
from graphene_django.types import DjangoObjectType
# from graphene_django.filter import DjangoFilterConnectionField

from django.contrib.auth.models import *


class UserWhereUniqueInput(graphene.InputObjectType):
    id = graphene.Int()


class UserWhereInput(UserWhereUniqueInput):
    AND = graphene.Field('core.schema.UserWhereInput')
    OR = graphene.Field('core.schema.UserWhereInput')
    email = graphene.String()


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        # filter_fields = ['email', ]
        # interfaces = (Node, )


class GroupNode(DjangoObjectType):
    class Meta:
        model = Group
        # filter_fields = ['name']
        # interfaces = (Node, )


class PermissionNode(DjangoObjectType):
    class Meta:
        model = Permission
        # filter_fields = ['name']
        # interfaces = (Node, )


def user_filter(queryset, where):
    if where is None:
        return queryset

    if where.get('AND'):
        queryset = user_filter(queryset, where.get('AND'))

    if where.get('OR'):
        queryset = queryset + user_filter(queryset, where.get('OR'))

    if where.get('email'):
        queryset = queryset.filter(email=where.get('email'))

    if where.get('id'):
        queryset = queryset.filter(id=where.get('id'))

    return queryset


class Query(object):
    all_users = graphene.List(UserNode, where=UserWhereInput(required=False))
    user = graphene.Field(UserNode, where=UserWhereUniqueInput(required=True))
    # all_users = DjangoFilterConnectionField(UserNode)

    def resolve_all_users(self, info, where=None):
        return user_filter(User.objects.all(), where)

    def resolve_user(self, info, where):
        return user_filter(User.objects.all(), where).first()


class Mutation(object):
    pass
