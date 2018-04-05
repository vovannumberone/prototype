from django.db import models
from django.contrib.auth.models import User

import json

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=100, null=True, blank=True)
    balance = models.IntegerField(null=True)

class ConnectedPublic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pid = models.IntegerField(unique=True)

class SourcePublic(models.Model):
    pid = models.IntegerField(unique=True)
    index = models.IntegerField(null=True)
