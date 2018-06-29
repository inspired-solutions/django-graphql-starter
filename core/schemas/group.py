import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import models as auth_models
from django.db.transaction import atomic

from djangographql.utils import model_filter
from core.schemas.permission import PermissionManyInput, connect_group


class GroupWhereUniqueInput(graphene.InputObjectType):
    id = graphene.ID()


class GroupWhereInput(GroupWhereUniqueInput):
    AND = graphene.Field('core.schemas.group.GroupWhereInput')
    OR = graphene.Field('core.schemas.group.GroupWhereInput')
    name = graphene.String()


class Group(DjangoObjectType):
    class Meta:
        model = auth_models.Group


class Query(graphene.ObjectType):
    groups = graphene.List(Group, where=GroupWhereInput())
    group = graphene.Field(Group, where=GroupWhereUniqueInput(required=True))

    def resolve_groups(self, info, where=None):
        return model_filter(auth_models.Group.objects.all(), where)

    def resolve_group(self, info, where):
        groups = model_filter(auth_models.Group.objects.all(), where)
        assert len(groups) < 2, 'Many Groups found.'
        assert len(groups) > 0, 'Group not found'
        return groups.first()


class GroupCreateInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    permissions = PermissionManyInput()


class GroupUpdateInput(graphene.InputObjectType):
    name = graphene.String()
    permissions = PermissionManyInput()


class OutputGroup(graphene.ObjectType):
    Output = Group


class CreateGroup(OutputGroup, graphene.Mutation):
    class Arguments:
        data = GroupCreateInput(required=True)

    @atomic
    def mutate(self, info, data):
        group = auth_models.Group()
        group.name = data.name
        group.save()

        connect_group(group, info, data)

        return group


class UpdateGroup(OutputGroup, graphene.Mutation):
    class Arguments:
        data = GroupUpdateInput(required=True)
        where = GroupWhereUniqueInput(required=True)

    @atomic
    def mutate(self, info, data, where):
        group = Query().resolve_group(info, where)

        if data.get('name'):
            group.name = data.name

        group.save()

        connect_group(group, info, data)

        return group


class DeleteGroup(OutputGroup, graphene.Mutation):
    class Arguments:
        where = GroupWhereUniqueInput(required=True)

    def mutate(self, info, where):
        group = Query().resolve_group(info, where)
        group.delete()
        return group


class Mutation(graphene.ObjectType):
    create_group = CreateGroup.Field()
    update_group = UpdateGroup.Field()
    delete_group = DeleteGroup.Field()
