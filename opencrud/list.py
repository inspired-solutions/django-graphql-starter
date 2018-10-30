import graphene

from graphene_django.utils import maybe_queryset

from django.db.models.query import QuerySet

from .filter import OpenCrudDjangoFilterConnectionField
from .utils import connection_from_list_slice


class OpenCrudDjangoFilterListField(OpenCrudDjangoFilterConnectionField):
    """ Custom List following OpenCrud specs """
    @property
    def type(self):
        """ returns List of given node type """
        from graphene_django.types import DjangoObjectType
        from graphene.relay.connection import ConnectionField

        _type = super(ConnectionField, self).type
        assert issubclass(
            _type, DjangoObjectType
        ), "DjangoConnectionField only accepts DjangoObjectType types"
        assert _type._meta.connection, "The type {} doesn't have a connection".format(
            _type.__name__
        )

        list = graphene.List(_type)
        list._meta = _type._meta.connection._meta

        return list

    @classmethod
    def resolve_connection(cls, connection, default_manager, args, iterable):
        """ Calls custom connection_from_list_slice with support for skip field """
        if iterable is None:
            iterable = default_manager
        iterable = maybe_queryset(iterable)
        if isinstance(iterable, QuerySet):
            if iterable is not default_manager:
                default_queryset = maybe_queryset(default_manager)
                iterable = cls.merge_querysets(default_queryset, iterable)
            _len = iterable.count()
        else:
            _len = len(iterable)

        connection = connection_from_list_slice(
            iterable,
            args,
            slice_start=0,
            list_length=_len,
            list_slice_length=_len,
            connection_type=connection,
            edge_type=None,
            pageinfo_type=None,
        )

        return connection
