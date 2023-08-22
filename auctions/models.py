from email.policy import default
from django.contrib.auth.models import User
from django.db import models


# Model for users, an extention of AbstractUser

# Model for Listings
class Listing(models.Model):
    seller = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    category = models.CharField(max_length=64)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_pic=models.ImageField(default="avatar_person.png", null=True,blank=True, upload_to='images/')

# Model for Comments
class Comment(models.Model):
    user = models.CharField(max_length=64)
    text = models.CharField(max_length=64)
    listing_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


# Model for Bids
class Bid(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    listing_id = models.IntegerField()
    bid = models.IntegerField()

# Model for Watchlist
class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listing_id = models.IntegerField()


# Model for Bid Winners
class Winner(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    listing_id = models.IntegerField()
    winprice = models.IntegerField()
    title = models.CharField(max_length=64, null=True)

# Model for contact message
class ContactMessage(models.Model):
    name = models.CharField(max_length=64)
    email= models.EmailField()
    message = models.TextField()