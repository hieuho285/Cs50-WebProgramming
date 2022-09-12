from asyncio.windows_events import NULL
from hashlib import blake2b
from pyexpat import model
from tkinter import CASCADE
from typing import List
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    pass

class Bid(models.Model):
    bid = models.FloatField(default=0)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user", default=None)
 
class Listing(models.Model):
    
    isClosed = models.BooleanField(default=False)
    title = models.CharField(max_length=64)
    image = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_winner", blank=True, null=True)
    startingBid = models.FloatField(default=0)   
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, related_name="listing_bid", default=None, null=True)
    category = models.CharField(max_length=50)
    watchList = models.ManyToManyField(User, blank=True, related_name="listing_watchlist")
    def __str__(self):
        return f"{self.title} {self.bid}"

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listing", default=None)
