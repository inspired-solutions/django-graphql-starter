import graphene

from collections import OrderedDict
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.utils import maybe_queryset
from graphene.types.argument import to_arguments
from graphene.relay import PageInfo

from django.db.models.query import QuerySet
from .utils import get_filterset_class, get_filtering_args_from_filterset, connection_from_list_slice


class CustomDjangoFilterConnectionField(DjangoFilterConnectionField):
    def __init__(
        self,
        *args,
        **kwargs
    ):
        self._order_by = kwargs['order_by']
        kwargs.setdefault("skip", graphene.Int())
        super(CustomDjangoFilterConnectionField, self).__init__(*args, **kwargs)

    @property
    def args(self):
        # if self._order_by
        '''where = type(
            str("%sWhereInput" % model._meta.object_name),
            (graphene.InputObjectType, ),
            {"Meta": meta_class},
        )'''
        return to_arguments(self._base_args or OrderedDict(), self.filtering_args)

    @args.setter
    def args(self, args):
        self._base_args = args

    @property
    def filterset_class(self):
        if not self._filterset_class:
            fields = self._fields or self.node_type._meta.filter_fields
            meta = dict(model=self.model, fields=fields, order_by=self._order_by)
            if self._extra_filter_meta:
                meta.update(self._extra_filter_meta)

            self._filterset_class = get_filterset_class(
                self._provided_filterset_class, **meta
            )

        return self._filterset_class

    @property
    def filtering_args(self):
        return get_filtering_args_from_filterset(self.filterset_class, self.node_type)

    @classmethod
    def resolve_connection(cls, connection, default_manager, args, iterable):
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
            edge_type=connection.Edge,
            pageinfo_type=PageInfo,
        )
        connection.iterable = iterable
        connection.length = _len
        return connection

    @classmethod
    def connection_resolver(
        cls,
        resolver,
        connection,
        default_manager,
        max_limit,
        enforce_first_or_last,
        filterset_class,
        filtering_args,
        root,
        info,
        **args
    ):
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(
            data=filter_kwargs,
            queryset=default_manager.get_queryset(),
            request=info.context,
        ).qs

        return super(DjangoFilterConnectionField, cls).connection_resolver(
            resolver,
            connection,
            qs,
            max_limit,
            enforce_first_or_last,
            root,
            info,
            **args
        )
