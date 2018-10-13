import graphene
from graphene_django.types import DjangoObjectType

from django.contrib.auth import models as auth_models
from graphene import Node

from djangographql.utils import model_filter

from opencrud.custom import CustomDjangoFilterConnectionField, WithCustomConnection


class UserWhereUniqueInput(graphene.InputObjectType):
    id = graphene.ID()


class User(DjangoObjectType):
    @WithCustomConnection(auth_models.User)
    class Meta:
        filter_fields = {
            'email': ('exact', 'contains', 'startswith', ),
        }
        interfaces = (Node, )


class User2(DjangoObjectType):
    @WithCustomConnection(auth_models.User)
    class Meta:
        filter_fields = ('email', )
        interfaces = (Node, )


class Query(graphene.ObjectType):
    # users = graphene.List(User, where=UserWhereInput())
    # user = graphene.Field(User, where=UserWhereUniqueInput(required=True))
    users_connection = CustomDjangoFilterConnectionField(User)
    foo = CustomDjangoFilterConnectionField(User)
    bar = CustomDjangoFilterConnectionField(User2)

    def resolve_users(self, info, where=None):
        return model_filter(auth_models.User.objects.all(), where)

    def resolve_user(self, info, where):
        users = model_filter(auth_models.User.objects.all(), where)
        assert len(users) < 2, 'Many Users found'
        assert len(users) > 0, 'User not found'
        return users.first()
