from django.test import TestCase

import graphene
from graphene_django.types import DjangoObjectType

from django.contrib.auth import models as auth_models
from graphene import Node, Schema

from .custom import CustomDjangoFilterConnectionField
from .utils import get_connection_class


class User(DjangoObjectType):
    class Meta:
        model = auth_models.User
        filter_fields = ('email', )
        interfaces = (Node, )
        connection_class = get_connection_class(auth_models.User)


class Query(graphene.ObjectType):
    users_connection_default = CustomDjangoFilterConnectionField(User, order_by=None)
    # users_connection_false = CustomDjangoFilterConnectionField(User, order_by=False)
    # users_connection_custom = CustomDjangoFilterConnectionField(User, order_by=('email', 'first_name', 'last_name', ))


schema = Schema(Query)


def execute(test, args=""):
    if args:
        args = "(" + args + ")"

    return schema.execute(
        """
            {
                usersConnection%s%s {
                    edges {
                        node {
                            id
                        }
                        cursor
                    }
                    pageInfo {
                        startCursor
                        endCursor
                    }
                }
            }
        """ % (test, args)
    )


def test_orderby_default():
    result = execute('Default', "orderBy:email_ASC")

    assert not result.errors

# test CustomDjangoFilterConnectionField
# test order_by
# test order_by False
# test order_by with fields
# test skip
# test where filter
# test multiple DjangoObjectType of same model
# test multiple CustomDjangoFilterConnectionField of same node
# test CustomDjangoFilterListField
# test CustomDjangoField
