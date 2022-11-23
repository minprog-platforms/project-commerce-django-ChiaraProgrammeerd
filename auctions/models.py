from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    image = models.CharField(max_length=300)
    price = models.FloatField()
    description = models.CharField(max_length=1000)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    pass

class Comment(models.Model):
    pass
