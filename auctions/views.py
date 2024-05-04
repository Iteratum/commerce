from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "data": listings,
    })


def categories_view(request, id):
    
    category = Category.objects.get(pk=id)
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/Categories_view.html", {
    "category_items": listings,
    "cat": category
})
        
@login_required
def listing_detail(request, id):
    listing_item = Listing.objects.get(pk=id)
    user_watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist_items = user_watchlist.items.all()
    bids = Bid.objects.filter(listing=listing_item).order_by('-created_at')
    latest_bidder = bids.first()

    if latest_bidder:
        latest_bidder = latest_bidder.bidder

    comments = Comment.objects.filter(listing=listing_item)
    creator = listing_item.creator
    user = request.user

    return render(request, "auctions/listing_detail.html", {
        "listing": listing_item,
        "watchlist_items": watchlist_items,
        "latest_bidder": latest_bidder,
        "comments": comments,
        "user": user,
        "creator": creator
    })

@login_required
def add_to_watchlist(request, item_id):
    item = get_object_or_404(Listing, pk=item_id)
    user_watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    user_watchlist.items.add(item)
    return redirect("watchlist")

@login_required
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

def category(request):
    category_options = Category.objects.all()
    if request.method == "GET":
        return render(request, "auctions/category.html", {
            "lists": category_options
        })

@login_required
def create_listing(request):
    category_options = Category.objects.all()
    if request.method == "POST" and "FILES":
        title = request.POST["title"]
        starting_bid = request.POST["starting_bid"]
        option = request.POST["category"]
        description = request.POST["description"]
        images = request.FILES["image"]
        creator = request.user
        new_listing = Listing.objects.create(
            title=title,
            description=description,
            starting_bid=starting_bid,
            current_bid=starting_bid,
            creator=creator,
            category = option
        )
        new_listing.save()
        return redirect("index")
    else:
        return render(request, "auctions/create_listing.html", {
            "options": category_options
        })

def place_bid(request):
    if request.method == 'POST':
        amount = float(request.POST["amount"])  # Convert amount to float
        listing_id = request.POST["item_id"]
        bidder = request.user
        
        listing = get_object_or_404(Listing, pk=listing_id)
        latest_bid = Bid.objects.filter(listing=listing).order_by('-created_at').first()
        
        if latest_bid and amount <= latest_bid.amount:
            # If the bid amount is lower than or equal to the latest bid
            messages.error(request, 'Your bid must be higher than the current bid.')
        else:
            # If the bid amount is higher, create a new bid
            new_bid = Bid.objects.create(
                listing=listing,
                bidder=bidder,
                amount=amount
            )
            new_bid.save()
            listing.current_bid = amount
            listing.save()
            messages.success(request, 'Bid placed successfully.')

        # Redirect back to the listing detail page
        return redirect('listing_detail', id=listing.id)

    # If the request method is not POST, return to the listing detail page
    return redirect('listing_detail', id=listing_id)

def add_comment(request):
    if request.method == 'POST':
        text = request.POST["text"]
        item_id = request.POST["item_id"]
        user = request.user
        listing = get_object_or_404(Listing, pk=item_id)

        new_comment = Comment.objects.create(
            listing=listing,
            user=user,
            text=text
        )
        new_comment.save()
        return redirect('listing_detail', id=listing.id)
    return render(request, 'listing_detail.html', {'listing': listing})

def close_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user == listing.creator:
        listing.is_active = False
        listing.save()
        return redirect(reverse('listing_detail', args=[listing.id]))
    else:
        # Handle the case where the user is not the creator of the listing
        return HttpResponseForbidden("You do not have permission to close this listing.")


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
            # Create a new user instance with the form data
            User = get_user_model()
            password = make_password(password)
            new_user = User(username=username, email=email, password=password)
            
            # Save the new user to the database
            new_user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, new_user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



