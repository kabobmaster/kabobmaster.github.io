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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default="open")
    #open/close status field, default to open, update to closed

class watchlist(models.Model):
    time = models.DateTimeField(default=datetime.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="people")
    watching = models.ForeignKey(listings, on_delete=models.CASCADE, related_name="watch")

class bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    listing = models.ForeignKey(listings, on_delete=models.CASCADE, null=True, blank=True)

class comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    listing = models.ForeignKey(listings, on_delete=models.CASCADE, null=True, blank=True)