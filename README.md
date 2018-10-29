<h1 align="center"><strong>Django with GraphQL Server</strong></h1>

![](https://cdn-images-1.medium.com/max/1600/1*jLrvxW83rre-25Nrhk-tww.png)

## Features

- **Django:** Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers,
it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.

- **Django Rest Framework** Django REST framework is a powerful and flexible toolkit for building Web APIs. <http://www.django-rest-framework.org/>

- **Graphql:** GraphQL is a query language for your API, and a server-side runtime for executing queries by using a type system you define for your data.
GraphQL isn't tied to any specific database or storage engine and is instead backed by your existing code and data.

- **Graphene:** A Django integration for Graphene. <https://github.com/graphql-python/graphene-django>

- **Django corsheaders** Django app for handling the server headers required for Cross-Origin Resource Sharing
(CORS) <https://github.com/ottoyiu/django-cors-headers>

## Requirements
You need to install [Python](https://www.python.org/downloads/) and add to your Path

## Getting started

```sh
# 1. Clone the project
git clone git@github.com:inspired-solutions/django-graphql-starter.git

# 2. Navigate to the new project
cd django-graphql-starter

# 3. Activate virtualenv
virtualenv venv -p /path/to/python3
. venv/bin/activate # linux
. venv/Scripts/activate # windows

# 4. Install modules
pip3 install -r requirements.txt

# 5. Apply Migrations
./manage.py migrate

# 6. Start server (runs on http://localhost:8000)
./manage.py runserver
```

## Documentation

### Commands

* `pip install -r requirements` Install all modules described in requirements.txt
* `python manage.py migrate` Apply migrations to database
* `python manage.py runserver` Start server

### Project structure
| File name | Description|
|:---|:---|
|`├── .gitignore`| Lists the files and directories that Git should ignore |
|`├── core`| |
|`│   ├── __init__.py`||
|`│   ├── admin.py`||
|`│   ├── apps.py`||
|`│   ├── migrations`||
|`│   │   └── __init__.py`||
|`│   ├── models.py`||
|`│   ├── schema.py`||
|`│   ├── schemas`||
|`│   │   ├── auth.py`||
|`│   │   ├── group.py`||
|`│   │   ├── permission.py`||
|`│   │   └── user.py`||
|`│   ├── tests.py`||
|`│   └── views.py`||
|`├── djangographql`| The <django_project_root> of the project |
|`│   ├── __init__.py`||
|`│   ├── local_settings.example.py`||
|`│   ├── local_settings.prod.py`||
|`│   ├── middleware.py`||
|`│   ├── schema.py`||
|`│   ├── settings.py`||
|`│   ├── urls.py`||
|`│   ├── utils.py`||
|`│   └── wsgi.py`||
|`├── manage.py`||
|`├── requirements.txt`| A list of Python packages required by your project, including the requirements.txt Django package |
|`└── tox.ini`||



## Deployment

```
$ cp djangographql/local_settings.prod.py djangographql/local_settings.py
$ nano djangographql/local_settings.py  # update settings
$ ./manage.py migrate
$ ./manage.py collectstatic
```

## References
- [https://www.djangoproject.com/](https://github.com/django/django)

## Contributing

The django-graphql-starter are maintained by the Inspired Solutions.

Your feedback is **very helpful**, please share your opinion and thoughts! If you have any questions or want to contribute yourself, join the [`#django-graphql-starter`](https://inspired-solutions.slack.com/messages/django-graphql-starter) channel on our [Slack](https://inspired-solutions.slack.com/).
