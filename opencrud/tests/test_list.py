import pytest
import graphene

from graphene_django.types import DjangoObjectType
from graphene import Node, Schema

from opencrud.tests import models
from opencrud.connection import WithOpenCrudConnection
from opencrud.list import OpenCrudDjangoFilterListField


pytestmark = pytest.mark.django_db


class User(DjangoObjectType):
    @WithOpenCrudConnection(models.User)
    class Meta:
        filter_fields = ('id', 'email', )
        interfaces = (Node, )


class Query(graphene.ObjectType):
    users = OpenCrudDjangoFilterListField(User)


schema = Schema(Query)


@pytest.mark.django_db
def create():
    models.User.objects.create(email="foo@bar.com", age=36)
    models.User.objects.create(email="me@email.com", age=32)


def test_list_result():
    create()
    result = schema.execute('''
        query {
            users {
                id
                email
            }
        }
    ''')

    assert not result.errors
    assert len(result.data['users']) == 2
    assert result.data['users'][0]['email'] == "foo@bar.com"


def test_skip():
    create()
    result = schema.execute('''
        query {
            users(skip: 1) {
                id
                email
            }
        }
    ''')

    assert not result.errors
    assert len(result.data['users']) == 1
    assert result.data['users'][0]['email'] == "me@email.com"


def test_order_by():
    create()
    result = schema.execute('''
        query {
            users(orderBy: email_DESC) {
                id
                email
            }
        }
    ''')

    assert not result.errors
    assert len(result.data['users']) == 2
    assert result.data['users'][0]['email'] == "me@email.com"


def test_where():
    create()
    result = schema.execute('''
        query {
            users(where: {email: "me@email.com"}) {
                id
                email
            }
        }
    ''')

    assert not result.errors
    assert len(result.data['users']) == 1
    assert result.data['users'][0]['email'] == "me@email.com"
