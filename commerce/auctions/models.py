from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    bid = models.FloatField()
    category = models.CharField(max_length=64)
    image = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.title}: {self.description}: {self.bid}: {self.category}: {self.image}"

class bids(models.Model):
    pass

class comments(models.Model):
    pass