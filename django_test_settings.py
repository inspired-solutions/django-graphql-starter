import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 1

INSTALLED_APPS = [
    'graphene_django',
    'opencrud',
    'opencrud.tests',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'django_test.sqlite'),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

GRAPHENE = {
    'SCHEMA': 'graphene_django.tests.schema_view.schema'
}
