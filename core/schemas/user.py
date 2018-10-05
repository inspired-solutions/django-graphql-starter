import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth import models as auth_models
from graphene import Node

from djangographql.utils import model_filter


class UserWhereUniqueInput(graphene.InputObjectType):
    id = graphene.ID()


class UserWhereInput(UserWhereUniqueInput):
    AND = graphene.Field('core.schemas.user.UserWhereInput')
    OR = graphene.Field('core.schemas.user.UserWhereInput')
    email = graphene.String()


class AggregateUser(graphene.ObjectType):
    count = graphene.Int()


class User(DjangoObjectType):
    class Meta:
        model = auth_models.User
        filter_fields = ('email', )
        interfaces = (Node, )


class Query(graphene.ObjectType):
    users = graphene.List(User, where=UserWhereInput())
    user = graphene.Field(User, where=UserWhereUniqueInput(required=True))
    usersConnection = DjangoFilterConnectionField(User)

    def resolve_users(self, info, where=None):
        return model_filter(auth_models.User.objects.all(), where)

    def resolve_user(self, info, where):
        users = model_filter(auth_models.User.objects.all(), where)
        assert len(users) < 2, 'Many Users found'
        assert len(users) > 0, 'User not found'
        return users.first()
