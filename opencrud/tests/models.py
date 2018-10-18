from django.db import models


class User(models.Model):
    email = models.CharField(max_length=30)
    age = models.IntegerField()
