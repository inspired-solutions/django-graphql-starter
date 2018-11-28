import graphene
from collections import OrderedDict
from graphene.types.argument import to_arguments
from graphene_django.registry import get_global_registry
from graphene_django.converter import convert_django_field_with_choices


def get_model_fields(model):
    local_fields = [
        (field.name, field)
        for field in sorted(
            list(model._meta.fields)  # + list(model._meta.local_many_to_many)
        )
    ]

    # Make sure we don't duplicate local fields with "reverse" version
    # local_field_names = [field[0] for field in local_fields]
    # reverse_fields = get_reverse_fields(model, local_field_names)

    all_fields = local_fields  # + list(reverse_fields)

    return all_fields


def construct_fields(model, registry, only_fields, exclude_fields):
    _model_fields = get_model_fields(model)

    fields = OrderedDict()
    for name, field in _model_fields:
        is_not_in_only = only_fields and name not in only_fields
        # is_already_created = name in options.fields
        is_excluded = name in exclude_fields  # or is_already_created
        # https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.ForeignKey.related_query_name
        is_no_backref = str(name).endswith("+")
        if is_not_in_only or is_excluded or is_no_backref:
            # We skip this field if we specify only_fields and is not
            # in there. Or when we exclude this field in exclude_fields.
            # Or when there is no back reference.
            continue
        converted = convert_django_field_with_choices(field, registry)
        fields[name] = converted

    return fields


def get_model_create_input_field(model):
    registry = get_global_registry()

    classname = str("%sCreateInput" % model._meta.object_name)

    input_class = registry._registry.get(classname)
    if not input_class:

        fields = construct_fields(model, registry, (), ('id',))

        input_class = type(
            classname,
            (graphene.InputObjectType,),
            fields,
        )

        registry._registry[classname] = input_class

    return graphene.NonNull(input_class)


class OpenCrudModelCreateField(graphene.Field):
    """ Model Create Field using OpenCrud specs """
    def __init__(self, type, *args, **kwargs):
        super(OpenCrudModelCreateField, self).__init__(type, *args, **kwargs)

    '''@property
    def args(self):
        """ Adds data field """
        data = get_model_create_input_field(self._type._meta.model)

        extra_args = {
            'data': data,
        }

        return to_arguments(self._base_args or OrderedDict(), extra_args)

    @args.setter
    def args(self, args):
        self._base_args = args'''

    @classmethod
    def Field(
        cls, type, name=None, description=None, deprecation_reason=None, required=False
    ):
        args = get_create_model_mutation(type._meta.model)

        return graphene.Field(
            type,
            # args=cls._meta.arguments,
            # resolver=cls._meta.resolver,
            name=name,
            description=description,
            deprecation_reason=deprecation_reason,
            required=required,
        )


def get_create_model_mutation(model):
    registry = get_global_registry()

    classname = str("Create%s" % model._meta.object_name)

    mutation_class = registry._registry.get(classname)
    if not mutation_class:
        fields = construct_fields(model, registry, (), ('id',))

        mutation_class = type(
            classname,
            (graphene.InputObjectType,),
            fields,
        )

        registry._registry[classname] = mutation_class

    return graphene.NonNull(mutation_class)

'''
class CreateUser(OutputUser, graphene.Mutation):
    class Arguments:
        data = UserCreateInput(required=True)

    def mutate(self, info, data):
        user = auth_models.User()
        user.email = data.email
        user.save()

        return user
'''
