<h1 align="center"><strong>Django with GraphQL Server</strong></h1>

![](https://cdn-images-1.medium.com/max/1600/1*jLrvxW83rre-25Nrhk-tww.png)

## Features

- **Django:** Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.

- **Django Rest Framework** Django REST framework is a powerful and flexible toolkit for building Web APIs. [`http://www.django-rest-framework.org/`]

- **Graphql:** GraphQL is a query language for your API, and a server-side runtime for executing queries by using a type system you define for your data. GraphQL isn't tied to any specific database or storage engine and is instead backed by your existing code and data.

- **Graphene:** A Django integration for Graphene.[`https://github.com/graphql-python/graphene-django`]

- **Django corsheaders** Django app for handling the server headers required for Cross-Origin Resource Sharing (CORS) [`https://github.com/ottoyiu/django-cors-headers`]

## Requirements
You need to install [Python](https://www.python.org/downloads/) and add to your Path

## Getting started
```
$ git clone git@github.com:inspired-solutions/django-graphql-starter.git
$ cd django-graphql-starter
$ virtualenv venv -p /path/to/python3
$ . venv/bin/activate (linux)
$ . venv/Scripts/activate (windows)
$ pip3 install -r requirements.txt
$ ./manage.py migrate
```

## Documentation

### Commands

* `pip install -r requirements` Install all modules described in requirements.txt
* `python manage.py migrate` Apply migrations to database
 

## Deployment
```
$ cp djangographql/local_settings.prod.py djangographql/local_settings.py
$ nano djangographql/local_settings.py  # update settings
$ ./manage.py migrate
$ ./manage.py collectstatic
```
