import pytest
import graphene

from graphene_django.types import DjangoObjectType
from graphene import Node, Schema

from opencrud.tests import models
from opencrud.connection import WithOpenCrudConnection
from opencrud.field import OpenCrudDjangoField


pytestmark = pytest.mark.django_db


class User(DjangoObjectType):
    @WithOpenCrudConnection(models.User)
    class Meta:
        filter_fields = ('id', 'email', )
        interfaces = (Node, )


@pytest.mark.django_db
def test_open_crud_django_field():
    models.User.objects.create(email="foo@bar.com", age=36)
    models.User.objects.create(email="me@email.com", age=32)

    class Query(graphene.ObjectType):
        user = OpenCrudDjangoField(User)

    schema = Schema(Query)

    result = schema.execute('''
        query {
            user(where: {id: "VXNlcjox"}) {
                id
                email
            }
        }
    ''')

    assert not result.errors
    assert result.data['user']['email'] == "foo@bar.com"
