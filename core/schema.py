import graphene
from graphene import Node, relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from django.contrib.auth.models import *

class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ['name']
        interfaces = (Node, )


class GroupNode(DjangoObjectType):
    class Meta:
        model = Group
        filter_fields = ['name']
        interfaces = (Node, )


class PermissionNode(DjangoObjectType):
    class Meta:
        model = Permission
        filter_fields = ['name']
        interfaces = (Node, )
