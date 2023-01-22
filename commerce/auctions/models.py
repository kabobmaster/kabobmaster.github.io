from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

class listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    bid = models.FloatField()
    category = models.CharField(max_length=64)
    image = models.CharField(max_length=1000)

class watchlist(models.Model):
    time = models.DateTimeField(default=datetime.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="people")
    watching = models.ForeignKey(listings, on_delete=models.CASCADE, related_name="watch")

class bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    listing = models.ForeignKey(listings, on_delete=models.CASCADE)

class comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    listing = models.ForeignKey(listings, on_delete=models.CASCADE)