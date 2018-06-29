import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import models as auth_models

from djangographql.utils import model_filter


class UserWhereUniqueInput(graphene.InputObjectType):
    id = graphene.ID()


class UserWhereInput(UserWhereUniqueInput):
    AND = graphene.Field('core.schemas.user.UserWhereInput')
    OR = graphene.Field('core.schemas.user.UserWhereInput')
    email = graphene.String()


class User(DjangoObjectType):
    class Meta:
        model = auth_models.User


class Query(graphene.ObjectType):
    users = graphene.List(User, where=UserWhereInput())
    user = graphene.Field(User, where=UserWhereUniqueInput(required=True))

    def resolve_users(self, info, where=None):
        return model_filter(auth_models.User.objects.all(), where)

    def resolve_user(self, info, where):
        user = model_filter(auth_models.User.objects.all(), where).first()
        assert user is not None, "User not found"
        return user
