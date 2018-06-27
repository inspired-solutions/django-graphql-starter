<h1 align="center"><strong>Django with GraphQL Server</strong></h1>

![](https://cdn-images-1.medium.com/max/1600/1*jLrvxW83rre-25Nrhk-tww.png)

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

## Deployment
```
$ cp djangographql/local_settings.prod.py djangographql/local_settings.py
$ nano djangographql/local_settings.py (update)
$ ./manage.py migrate
$ ./manage.py collectstatic
```
