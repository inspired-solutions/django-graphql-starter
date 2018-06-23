from rest_framework.authentication import TokenAuthentication


class TokenAuthenticationMiddleware:
    def resolve(self, next, root, info, **args):
        if root is None:
            result = TokenAuthentication().authenticate(info.context)

            assert result is not None, 'Authentication credentials were not provided.'

            user, token = result

            info.context.user = user
        return next(root, info, **args)
