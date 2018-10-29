from rest_framework.authentication import TokenAuthentication


class TokenAuthenticationMiddleware(object):
    def resolve(self, next, root, info, **args):

        if root is None:
            token_exempt = getattr(next.args[0], 'token_exempt', False)
            is_introspection = getattr(info.operation.name, 'value', False) == 'IntrospectionQuery'

            if not token_exempt and not is_introspection:
                result = TokenAuthentication().authenticate(info.context)

                assert result is not None, 'Authentication credentials were not provided.'

                user, token = result

                info.context.user = user

        return next(root, info, **args)


class ACLMiddleware(object):
    def resolve(self, next, root, info, **args):
        return next(root, info, **args)
