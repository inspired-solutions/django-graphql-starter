import graphene
from graphene_django.types import DjangoObjectType

from django.contrib.auth import models as auth_models
from graphene import Node

from opencrud.connection import WithOpenCrudConnection
from opencrud.list import OpenCrudDjangoFilterListField
from opencrud.filter import OpenCrudDjangoFilterConnectionField
from opencrud.field import OpenCrudDjangoField


from ..custom import OpenCrudModelCreateField


class User(DjangoObjectType):
    @WithOpenCrudConnection(auth_models.User)
    class Meta:
        filter_fields = ('id', 'email', )
        interfaces = (Node, )


class Query(graphene.ObjectType):
    user = OpenCrudDjangoField(User)
    users = OpenCrudDjangoFilterListField(User)
    users_connection = OpenCrudDjangoFilterConnectionField(User)


class UserCreateInput(graphene.InputObjectType):
    email = graphene.String(required=True)


class UserUpdateInput(graphene.InputObjectType):
    email = graphene.String()


class OutputUser(graphene.ObjectType):
    Output = User


# '''
from graphene_django.rest_framework.mutation import SerializerMutation
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = auth_models.User
        fields = '__all__'


class UserModelMutation(SerializerMutation):
    class Meta:
        serializer_class = UserSerializer
        # model_operations = ['create', 'update']
        # lookup_field = 'id'
        # '''


class CreateUser(OutputUser, graphene.Mutation):
    class Arguments:
        data = UserCreateInput(required=True)

    def mutate(self, info, data):
        user = auth_models.User()
        user.email = data.email
        user.save()

        return user


class Mutation(graphene.ObjectType):
    # user_mutation = UserModelMutation.Field()
    # create_user = CreateUser.Field()
    create_user = OpenCrudModelCreateField.Field(User)
