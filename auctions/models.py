from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    cat_choices = [
        ('Cl', 'Clothing'),
        ('Fn', 'Furnitures'),
        ('Jw', 'Jewelries')
    ]
    type = models.CharField(max_length=3, choices=cat_choices)
    
    
class Comments(models.Model):
    pass


class Bids(models.Model):
    pass


class Watchlist(models.Model):
    pass


class Listing(models.Model):
    product_name = models.CharField(max_length=64, verbose_name="product name")
    product_description = models.TextField(max_length=200, verbose_name="product description")
    product_image = models.URLField(null=False, verbose_name="image")
    product_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    is_active = models.BooleanField(blank=False, default=True)
    price_bid = models.DecimalField(decimal_places=2, max_digits=6)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")