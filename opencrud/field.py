import graphene

from functools import partial
from collections import OrderedDict
from graphene.types.argument import to_arguments
from graphene.relay.node import from_global_id

from .utils import get_where_unique_input_field


class OpenCrudDjangoField(graphene.Field):
    """ Custom Django Field following OpenCrud specs """
    def __init__(self, type, *args, **kwargs):
        super(OpenCrudDjangoField, self).__init__(type, *args, **kwargs)

    @property
    def args(self):
        """ Adds where field """
        where = get_where_unique_input_field(self._type._meta.model)

        extra_args = {
            'where': where,
        }

        return to_arguments(self._base_args or OrderedDict(), extra_args)

    @args.setter
    def args(self, args):
        self._base_args = args

    @classmethod
    def resolve_connection(cls, type, args, model_object):
        """ Uses parent_resolver, or resolves from global_id """
        name, id = from_global_id(args['where']['id'])

        if model_object is None:
            model_object = type._meta.model._default_manager.get(id=id)

        return model_object

    @classmethod
    def connection_resolver(
            cls,
            resolver,
            type,
            root,
            info,
            **args
    ):
        """ Calls cls.resolve_connection """
        model_object = resolver(root, info, **args)
        on_resolve = partial(cls.resolve_connection, type, args)

        return on_resolve(model_object)

    def get_resolver(self, parent_resolver):
        """ Calls self.connection_resolver """
        return partial(
            self.connection_resolver,
            parent_resolver,
            self.type,
        )
