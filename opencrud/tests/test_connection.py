import pytest
import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.fields import DjangoConnectionField
from graphene import Node, Schema

from opencrud.tests import models
from opencrud.connection import WithOpenCrudConnection


pytestmark = pytest.mark.django_db


class User(DjangoObjectType):
    @WithOpenCrudConnection(models.User)
    class Meta:
        filter_fields = ('id', 'email', )
        interfaces = (Node, )


def test_with_open_crud_connection():
    assert User._meta.model == models.User, "Expected model in User Meta"
    assert User._meta.connection._meta.name == 'UserConnection', "Expected UserConnection"


def test_get_connection_class():
    aggregate = User._meta.connection.aggregate

    assert aggregate._type._meta.name == 'AggregateUser', ""
    assert isinstance(aggregate._type.count, graphene.Int), ""


@pytest.mark.django_db
def test_connection():
    models.User.objects.create(email="foo@bar.com", age=36)

    class Query(graphene.ObjectType):
        users = DjangoConnectionField(User)

    schema = Schema(Query)

    result = schema.execute('''
        query {
            users {
                aggregate {
                    count
                }
            }
        }
    ''')

    assert not result.errors
    assert result.data['users']['aggregate']['count'] == 1
