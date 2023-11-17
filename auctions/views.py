from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json

from .models import *
from .forms import ListingForm


def index(request):
    listings = Listing.objects.filter(is_active=True)
    product_ca = Category.objects.all()
    return render(request, "auctions/index.html", {
        "data": listings,
        "categ": product_ca
    })


def categories_view(request):
    if request.method == "POST":
        category_name = request.POST["categorys"]
        category = Category.objects.get(type=category_name)
        listings = Listing.objects.filter(category=category)
        return render(request, "auctions/Categories_view.html", {
        "category": listings,
        "category_name": category_name,
        "cat": category
    })
        

def listing_view(request, id):
    listing_item = Listing.objects.get(pk=id)
    current_user = request.user
    user_watchlist = Watchlist.objects.get(user=current_user)
    watchlist_items = user_watchlist.items.all()
    return render(request, "auctions/listing_view.html", {
        "listing": listing_item,
        "watchlist_items": watchlist_items,
    })

def add_to_watchlist(request, item_id):
    item = get_object_or_404(Listing, pk=item_id)
    user_watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    user_watchlist.items.add(item)
    return redirect("watchlist")

def remove_from_watchlist(request, item_id):
    item = get_object_or_404(Listing, pk=item_id)
    current_user = request.user
    user_watchlist = Watchlist.objects.get(user=current_user)
    user_watchlist.items.remove(item)
    return redirect("watchlist")

def watchlist(request):
    user_watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist_items = user_watchlist.items.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })

def place_bid(request):
    if request.method == "POST":
        #data = json.loads(request.body)
        
        #create and save the bid value
        item_id = request.POST("item_id")
        bid_value = request.POST("bid_value")
        listing_item_id = get_object_or_404(Listing, pk=item_id)
        Bids.objects.create(bidder=request.user, bid_price=bid_value, listing_id=listing_item_id)
        listing_item_id.initial_price = bid_value
        listing_item_id.save()
        return render(request, "auctions/listing_view.html", {
            "price": bid_value,
            "message": "Your bid has been placed successfully"
        })
   

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        list = ListingForm(request.POST, request.FILES)
        if list.is_valid():
            product_name = list.cleaned_data["product_name"]
            product_image = list.cleaned_data["product_image"]
            initial_price = list.cleaned_data["initial_price"]
            product_category = list.cleaned_data["category"]
            owner = request.user
            listing = Listing(product_name=product_name, product_image=product_image, initial_price=initial_price, category=product_category, owner=owner)
            listing.save()
            List = Listing.objects.all
            return HttpResponseRedirect(reverse("index"))
    else:
        L_form = ListingForm
        return render(request, "auctions/create_listing.html", {
            "forms": L_form
        })

