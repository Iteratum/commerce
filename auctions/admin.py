from django.contrib import admin

# Register your models here.
from .models import User, Category, Comments, Listing

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Listing)