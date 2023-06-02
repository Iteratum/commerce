from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Listing(models.Model):
    category = [
        ('Cl', 'Clothing'),
        ('Fn', 'Furnitures'),
        ('Jw', 'Jewelries')
    ]
    product_name = models.CharField(max_length=64, verbose_name="product name")
    product_description = models.TextField(max_length=200, verbose_name="product description")
    product_image = models.ImageField(upload_to="images/", verbose_name="image")
    product_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(blank=False, default=True)
    price_bid = models.DecimalField(decimal_places=2, max_digits=6, default=0.00)
    product_category = models.CharField(verbose_name="Product Category", choices=category, max_length=2)
    
    
    
class Comments(models.Model):
    user_comment = models.TextField()
    user_id = models.ForeignKey(User, default=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user_comment
    


class Bids(models.Model):
    listing_id = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.listing_id
    


class Watchlist(models.Model):
    listing_id = models.ForeignKey(Listing, default=True, on_delete=models.CASCADE)