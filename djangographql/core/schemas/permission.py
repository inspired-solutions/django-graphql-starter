import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import models as auth_models

from djangographql.utils import model_filter


class PermissionWhereUniqueInput(graphene.InputObjectType):
    id = graphene.ID()


class PermissionWhereInput(PermissionWhereUniqueInput):
    AND = graphene.Field('core.schemas.permission.PermissionWhereInput')
    OR = graphene.Field('core.schemas.permission.PermissionWhereInput')
    name = graphene.String()
    codename = graphene.String()


class Permission(DjangoObjectType):
    class Meta:
        model = auth_models.Permission


class Query(graphene.ObjectType):
    permissions = graphene.List(Permission, where=PermissionWhereInput())
    permission = graphene.Field(Permission, where=PermissionWhereUniqueInput(required=True))

    def resolve_permissions(self, info, where=None):
        return model_filter(auth_models.Permission.objects.all(), where)

    def resolve_permission(self, info, where):
        permissions = model_filter(auth_models.Permission.objects.all(), where)
        assert len(permissions) < 2, 'Many Permissions found.'
        assert len(permissions) > 0, 'Permission not found'
        return permissions.first()


class PermissionCreateInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    codename = graphene.String(required=True)


class PermissionManyInput(graphene.InputObjectType):
    create = graphene.List(graphene.NonNull(PermissionCreateInput))
    connect = graphene.List(graphene.NonNull(PermissionWhereUniqueInput))


class PermissionUpdateInput(PermissionCreateInput):
    name = graphene.String()
    codename = graphene.String()


class OutputPermission(graphene.ObjectType):
    Output = Permission


class CreatePermission(OutputPermission, graphene.Mutation):
    class Arguments:
        data = PermissionCreateInput(required=True)

    def mutate(self, info, data):
        permission = auth_models.Permission()
        permission.name = data.name
        permission.codename = data.codename
        permission.content_type_id = 1
        permission.save()

        return permission


class UpdatePermission(OutputPermission, graphene.Mutation):
    class Arguments:
        data = PermissionUpdateInput(required=True)
        where = PermissionWhereUniqueInput(required=True)

    def mutate(self, info, data, where):
        permission = Query.resolve_permission(info, where)

        if data.get('name'):
            permission.name = data.name

        if data.get('codename'):
            permission.codename = data.codename

        permission.save()

        return permission


class Mutation(graphene.ObjectType):
    pass


def connect_group(group, info, data):
    permissions = data.get('permissions')

    if permissions:
        create = permissions.get('create')
        connect = permissions.get('connect')

        if create:
            for permission in create:
                model_permission = CreatePermission().mutate(info, permission)
                model_permission.group_set.add(group)

        if connect:
            for permission in connect:
                model_permission = Query().resolve_permission(info, permission)
                model_permission.group_set.add(group)
