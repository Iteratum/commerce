from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

class Category(models.Model):
    type = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.type

from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    options = [
        ("Co", "Clothing"),
        ("PH", "Phones"),
        ("FR", "Furnitures"),
    ]
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    starting_bid = models.DecimalField(max_digits=10, default=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, null=True, decimal_places=2)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    category = models.CharField(choices=options, max_length=5, blank=False, null=True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.amount

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.te

class Watchlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Listing, null=True, related_name="watchlist_item")

    def __str__(self):
        return self.items