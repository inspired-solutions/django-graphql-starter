import pytest
import graphene

from graphene_django.types import DjangoObjectType
from graphene import Node, Schema

from opencrud.tests import models
from opencrud.connection import WithOpenCrudConnection
from opencrud.filter import OpenCrudDjangoFilterConnectionField


pytestmark = pytest.mark.django_db


class User(DjangoObjectType):
    @WithOpenCrudConnection(models.User)
    class Meta:
        filter_fields = ('id', 'email', )
        interfaces = (Node, )


class Query(graphene.ObjectType):
    usersConnection = OpenCrudDjangoFilterConnectionField(User)


schema = Schema(Query)


@pytest.mark.django_db
def create():
    models.User.objects.create(email="foo@bar.com", age=36)
    models.User.objects.create(email="me@email.com", age=32)


def test_filter_result():
    create()
    result = schema.execute('''
        query {
            usersConnection {
                aggregate {
                    count
                }
            }
        }
    ''')

    assert not result.errors
    assert result.data['usersConnection']['aggregate']['count'] == 2
