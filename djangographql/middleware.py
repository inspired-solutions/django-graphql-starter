from rest_framework.authentication import TokenAuthentication


class TokenAuthenticationMiddleware(object):
    def resolve(self, next, root, info, **args):
        token_exempt = getattr(next.args[0], 'token_exempt', False)

        if root is None and not token_exempt:
            result = TokenAuthentication().authenticate(info.context)

            assert result is not None, 'Authentication credentials were not provided.'

            user, token = result

            info.context.user = user
        return next(root, info, **args)
