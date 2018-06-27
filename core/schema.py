import graphene
from graphene_django.types import DjangoObjectType

from django.contrib.auth import models as auth_models


class UserWhereUniqueInput(graphene.InputObjectType):
    id = graphene.ID()


class UserWhereInput(UserWhereUniqueInput):
    AND = graphene.Field('core.schema.UserWhereInput')
    OR = graphene.Field('core.schema.UserWhereInput')
    email = graphene.String()


class User(DjangoObjectType):
    class Meta:
        model = auth_models.User


class GroupWhereUniqueInput(graphene.InputObjectType):
    id = graphene.ID()


class GroupWhereInput(UserWhereUniqueInput):
    AND = graphene.Field('core.schema.GroupWhereInput')
    OR = graphene.Field('core.schema.GroupWhereInput')
    name = graphene.String()


class Group(DjangoObjectType):
    class Meta:
        model = auth_models.Group


class Permission(DjangoObjectType):
    class Meta:
        model = auth_models.Permission


def model_filter(queryset, where):
    if where is None:
        return queryset

    if where.get('AND'):
        queryset = model_filter(queryset, where.get('AND'))

    if where.get('OR'):
        queryset = queryset + model_filter(queryset, where.get('OR'))

    if where.get('email'):
        queryset = queryset.filter(email=where.get('email'))

    if where.get('name'):
        queryset = queryset.filter(name=where.get('name'))

    if where.get('id'):
        queryset = queryset.filter(id=where.get('id'))

    return queryset


class Query(graphene.ObjectType):
    users = graphene.List(User, where=UserWhereInput())
    user = graphene.Field(User, where=UserWhereUniqueInput(required=True))

    groups = graphene.List(Group, where=GroupWhereInput())
    group = graphene.Field(Group, where=GroupWhereUniqueInput(required=True))

    def resolve_users(self, info, where=None):
        return model_filter(auth_models.User.objects.all(), where)

    def resolve_user(self, info, where):
        return model_filter(auth_models.User.objects.all(), where).first()

    def resolve_groups(self, info, where=None):
        return model_filter(auth_models.Group.objects.all(), where)

    def resolve_group(self, info, where):
        return model_filter(auth_models.Group.objects.all(), where).first()


class PermissionCreateInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    codename = graphene.String(required=True)


class PermissionWhereUniqueInput(graphene.InputObjectType):
    id = graphene.ID()


class PermissionWhereInput(PermissionWhereUniqueInput):
    name = graphene.String()
    codename = graphene.String()


class PermissionManyInput(graphene.InputObjectType):
    create = graphene.List(graphene.NonNull(PermissionCreateInput))
    connect = graphene.List(graphene.NonNull(PermissionWhereUniqueInput))

    def mutate(self, info, data):
        pass


class GroupCreateInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    permissions = PermissionManyInput()
    # users = graphene.List(graphene.NonNull(UserManyInput))


class GroupUpdateInput(GroupCreateInput):
    name = graphene.String()
    permissions = graphene.List(graphene.NonNull(PermissionManyInput))


class OutputGroup(graphene.ObjectType):
    Output = Group


class CreateGroup(OutputGroup, graphene.Mutation):
    class Arguments:
        data = GroupCreateInput(required=True)

    def mutate(self, info, data):
        group = auth_models.Group()
        group.name = data.name
        group.save()

        permissions = data.get('permissions')

        if permissions:
            create = permissions.get('create')

            if create:
                for permission in create:
                    model_permission = auth_models.Permission()
                    model_permission.name = permission.name
                    model_permission.codename = permission.codename
                    model_permission.content_type_id = 1
                    model_permission.save()
                    model_permission.group_set.add(group)

        return group


class UpdateGroup(OutputGroup, graphene.Mutation):
    class Arguments:
        data = GroupUpdateInput(required=True) 
        where = GroupWhereUniqueInput(required=True)

    def mutate(self, info, data, where):
        try:
            group = auth_models.Group.objects.get(id=where.id)

            if where.get('name'):
                group.name = where.get('name')

            group.save()

            if where.get('permissions'):
                permissions = where.get('permissions')

                if permissions.get('connect'):
                    connect = permissions.get('connect')

                    for permission in connect:
                        try:
                            model_permission = auth_models.Permission.objects.get(id=permission.id)
                            model_permission.group_set.add(group)
                        except auth_models.Permission.DoesNotExists:
                            raise Exception('Permission not found.')

            return group
        except auth_models.Group.DoesNotExists:
            raise Exception('Group not found.')


class DeleteGroup(OutputGroup, graphene.Mutation):
    class Arguments:
        where = GroupWhereUniqueInput(required=True)

    def mutate(self, info, where):
        group = auth_models.Group.objects.get(id=where.id)
        group.delete()

        return group


class Mutation(graphene.ObjectType):
    create_group = CreateGroup.Field()
    update_group = UpdateGroup.Field()
    delete_group = DeleteGroup.Field()
