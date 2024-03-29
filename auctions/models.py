from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    type = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.type
    

class Listing(models.Model):
    product_name = models.CharField(max_length=64, verbose_name="product_name")
    product_description = models.TextField(max_length=200, verbose_name="product description")
    product_image = models.ImageField(upload_to="images/", verbose_name="image", blank=True)
    is_active = models.BooleanField(blank=False, default=True)
    initial_price = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    owner = models.ForeignKey(User, related_name="auction_owner", on_delete=models.CASCADE, default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    
    def __str__(self):
        return self.product_name
    
    
class Comments(models.Model):
    user_comment = models.TextField()
    user_id = models.ForeignKey(User, default=True, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user_comment
    


class Bids(models.Model):
    bidder = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    bid_price = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    listing_id = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.bid_price
    


class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    items = models.ManyToManyField(Listing, null=True, related_name="watchlist_item")

    def __str__(self):
        return self.items