""" Local settings for djangographql project. """

from .base import *

DEBUG = True

ENVIRONMENT = 'local'

ALLOWED_HOSTS = ['*']

# INSTALLED_APPS.append('sample')

# MIDDLEWARE.append('sample.middleware')

# DATABASES['OPTIONS'].update{ 'unix_socket': '/tmp/mysql/mysql.sock'}

# FIXTURES_PATH = os.path.join(os.path.dirname(BASE_DIR + '../path_to_fixtures/'), 'fixtures.json')
