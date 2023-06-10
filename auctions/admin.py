from django.contrib import admin

# Register your models here.
from .models import User, Comments, Listing, Bids, Category, Watchlist

admin.site.register(User)
admin.site.register(Comments)
admin.site.register(Listing)
admin.site.register(Bids)
admin.site.register(Category)
admin.site.register(Watchlist)