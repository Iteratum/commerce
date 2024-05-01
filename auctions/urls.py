from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("categories_view/<int:id>", views.categories_view, name="categories_view"),
    path("listing_detail/<int:id>", views.listing_detail, name="listing_detail"),
    path("add_to_watchlist/<int:item_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/(<int:item_id>)", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("place_bid", views.place_bid, name="place_bid"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("close_listing/(<int:listing_id>)", views.close_listing, name="close_listing"),
    path("category", views.category, name="category"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
