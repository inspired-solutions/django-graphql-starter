import graphene
from graphene_django import DjangoObjectType
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken import models as rest_models

from djangographql.utils import token_exempt


class Token(DjangoObjectType):
    class Meta:
        model = rest_models.Token


class OutputToken(graphene.ObjectType):
    Output = Token


class UserLoginInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)


class LoginUser(OutputToken, graphene.Mutation):
    class Arguments:
        data = UserLoginInput(required=True)

    @token_exempt
    def mutate(self, info, data):
        serializer = AuthTokenSerializer(data=data, context={'request': info.context})

        assert serializer.is_valid(), 'Unable to log in with provided credentials.'

        user = serializer.validated_data['user']
        token, created = rest_models.Token.objects.get_or_create(user=user)

        return token
        # mutate.token_exempt = True


class LogoutUser(OutputToken, graphene.Mutation):
    class Arguments:
        pass

    def mutate(self, info):
        user = info.context.user
        user.auth_token.delete()


class Mutation(graphene.ObjectType):
    login = LoginUser.Field()
    logout = LogoutUser.Field()
