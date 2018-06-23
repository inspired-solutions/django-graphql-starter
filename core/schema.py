# import graphene
from graphene import Node
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


from django.contrib.auth.models import *


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ['email', ]
        interfaces = (Node, )


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


class Query(object):
    # all_users = graphene.List(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

    '''def resolve_all_users(self, info, **kwargs):
        return User.objects.all()'''


class Mutation(object):
    pass
