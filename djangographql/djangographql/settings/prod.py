""" Local settings for djangographql project. """

from .base import *
import os

DEBUG = False

ENVIRONMENT = 'prod'

ALLOWED_HOSTS = []

# INSTALLED_APPS.append('sample')
# MIDDLEWARE.append('sample.middleware')
DATABASES['OPTIONS'].update{ 'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock'}