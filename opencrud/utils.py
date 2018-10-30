import six
import graphene

from graphene_django.filter.filterset import setup_filterset, GrapheneFilterSetMixin
from graphene_django.registry import get_global_registry
from graphql_relay.connection.connectiontypes import Connection, PageInfo, Edge
from graphql_relay.connection.arrayconnection import get_offset_with_default, offset_to_cursor
from graphene.types.argument import to_arguments

from django_filters import FilterSet, OrderingFilter


def _get_aggregate_class(name, registry):
    """ Get the aggregate class as a subclass of ObjectType """
    classname = str("Aggregate%s" % name)

    aggregate_class = registry._registry.get(classname)
    if not aggregate_class:
        aggregate_class = type(
            classname,
            (graphene.ObjectType,),
            {'count': graphene.Int()}
        )

        registry._registry[classname] = aggregate_class

    return aggregate_class


def get_connection_class(model):
    """ Get the connection class as a subclass of Connection """
    registry = get_global_registry()
    name = model._meta.object_name

    aggregate_class = _get_aggregate_class(name, registry)

    def resolve_aggregate(self, info):
        return aggregate_class(count=self.length)

    classname = str("%sConnection" % name)

    connection_class = registry._registry.get(classname)
    if not connection_class:
        connection_class = type(
            classname,
            (graphene.Connection, ),
            {
                'aggregate': graphene.Field(aggregate_class),
                'resolve_aggregate': resolve_aggregate,
                'Meta': {'abstract': True},
            }
        )

        registry._registry[classname] = connection_class

    return connection_class


def get_where_unique_input_field(model):
    """ Get the where input field as a subclass of InputObjectType """
    registry = get_global_registry()

    classname = str("%sWhereUniqueInput" % model._meta.object_name)

    where_class = registry._registry.get(classname)
    if not where_class:
        where_class = type(
            classname,
            (graphene.InputObjectType, ),
            {'id': graphene.ID(required=True)},
        )

        registry._registry[classname] = where_class

    return graphene.NonNull(where_class)


def get_where_input_field(filter_fields, model):
    """ Get the where input field as a subclass of InputObjectType """
    registry = get_global_registry()

    classname = str("%sWhereInput" % model._meta.object_name)

    where_class = registry._registry.get(classname)
    if not where_class:
        where_class = type(
            classname,
            (graphene.InputObjectType, ),
            to_arguments(filter_fields),
        )

        registry._registry[classname] = where_class

    return where_class()


def get_ordering_field(filter_field, model):
    """ Get the ordering fields as Enum """
    registry = get_global_registry()

    args = {}
    for choice in filter_field.field.choices.choices:
        field_name, label = choice

        suffix = 'DESC' if field_name.startswith('-') else 'ASC'
        name = '{}_{}'.format(field_name.replace('-', ''), suffix)

        args[name] = field_name

    classname = str("%sOrderByInput" % model._meta.object_name)

    order_class = registry._registry.get(classname)
    if not order_class:
        order_class = type(
            classname,
            (graphene.Enum, ),
            args
        )

        registry._registry[classname] = order_class

    return order_class()


def get_filtering_args_from_filterset(filterset_class, type):
    """ Inspect a FilterSet and produce the arguments to pass to
        a Graphene Field. These arguments will be available to
        filter against in the GraphQL
    """
    from graphene_django.forms.converter import convert_form_field

    args = {}
    for name, filter_field in six.iteritems(filterset_class.base_filters):

        if isinstance(filter_field, OrderingFilter):
            field_type = get_ordering_field(filter_field, type._meta.model)
        else:
            field_type = convert_form_field(filter_field.field).Argument()

        field_type.description = filter_field.label
        args[name] = field_type

    return args


def get_filterset_class(filterset_class, **meta):
    """Get the class to be used as the FilterSet"""
    if filterset_class:
        # If were given a FilterSet class, then set it up and
        # return it
        return setup_filterset(filterset_class)
    return custom_filterset_factory(**meta)


def custom_filterset_factory(model, filterset_base_class=FilterSet, order_by=None, **meta):
    """ Create a filterset for the given model using the provided meta data
    """
    meta.update({"model": model})
    meta_class = type(str("Meta"), (object,), meta)

    meta_dict = dict(Meta=meta_class)

    assert order_by in [None, False], \
        'order_by field can only be None or False'

    if order_by is None:
        order_by = tuple(field.name for field in model._meta.fields)

    if order_by:
        meta_dict.update({'order_by': OrderingFilter(fields=order_by)})

    filterset = type(
        str("%sFilterSet" % model._meta.object_name),
        (filterset_base_class, GrapheneFilterSetMixin),
        meta_dict,
    )
    return filterset


def connection_from_list_slice(list_slice, args=None, connection_type=None,
                               edge_type=None, pageinfo_type=None,
                               slice_start=0, list_length=0, list_slice_length=None):
    '''
    Given a slice (subset) of an array, returns a connection object for use in
    GraphQL.
    This function is similar to `connectionFromArray`, but is intended for use
    cases where you know the cardinality of the connection, consider it too large
    to materialize the entire array, and instead wish pass in a slice of the
    total result large enough to cover the range specified in `args`.
    '''
    connection_type = connection_type or Connection
    edge_type = edge_type or Edge
    pageinfo_type = pageinfo_type or PageInfo

    args = args or {}

    before = args.get('before')
    after = args.get('after')
    first = args.get('first')
    last = args.get('last')
    skip = args.get('skip', 0)
    if list_slice_length is None:
        list_slice_length = len(list_slice)
    slice_end = slice_start + list_slice_length
    before_offset = get_offset_with_default(before, list_length)
    after_offset = get_offset_with_default(after, -1)

    start_offset = max(
        slice_start - 1,
        skip - 1,
        after_offset,
        -1
    ) + 1
    end_offset = min(
        slice_end,
        before_offset,
        list_length
    )
    if isinstance(first, int):
        end_offset = min(
            end_offset,
            start_offset + first
        )
    if isinstance(last, int):
        start_offset = max(
            start_offset,
            end_offset - last
        )

    # If supplied slice is too large, trim it down before mapping over it.
    _slice = list_slice[
        max(start_offset - slice_start, 0):
        list_slice_length - (slice_end - end_offset)
    ]
    edges = [
        edge_type(
            node=node,
            cursor=offset_to_cursor(start_offset + i)
        )
        for i, node in enumerate(_slice)
    ]

    first_edge_cursor = edges[0].cursor if edges else None
    last_edge_cursor = edges[-1].cursor if edges else None
    lower_bound = after_offset + 1 if after else 0
    upper_bound = before_offset if before else list_length

    if isinstance(connection_type, graphene.List):
        return _slice
    else:
        return connection_type(
            edges=edges,
            page_info=pageinfo_type(
                start_cursor=first_edge_cursor,
                end_cursor=last_edge_cursor,
                has_previous_page=isinstance(last, int) and start_offset > lower_bound,
                has_next_page=isinstance(first, int) and end_offset < upper_bound
            )
        )
