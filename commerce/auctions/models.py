from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    bid = models.FloatField(max=1000000)
    category = models.CharField(max_length=64)
    image = models.CharField(max_length=1000)

class bids(models.Model):
    pass

class comments(models.Model):
    pass