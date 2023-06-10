from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category
from .forms import ListingForm


def index(request):
    listings = Listing.objects.filter(is_active=True)
    product_ca = Category.objects.all
    return render(request, "auctions/index.html", {
        "data": listings,
        "categ": product_ca
    })


def Categories_view(request):
    pass

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
            price_bid = list.cleaned_data["price_bid"]
            product_category = list.cleaned_data["product_category"]
            listing = Listing(product_name=product_name, product_image=product_image, price_bid=price_bid, product_category=product_category)
            listing.save()
            List = Listing.objects.all
            return HttpResponseRedirect(reverse("index"))
    else:
        L_form = ListingForm
        return render(request, "auctions/create_listing.html", {
            "forms": L_form
        })