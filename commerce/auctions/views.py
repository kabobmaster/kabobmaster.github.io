from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from auctions.models import *

from .models import User

CATEGORY = [
    ('Appliance', 'Appliance'),
    ('Furniture', "Furniture"),
    ('Electronics', 'Electronics'),
    ('Cars', 'Cars'),
    ('Sports', 'Sports'),
    ('Games', 'Games'),
    ('Home', 'Home'),
    ('Other', 'Other')
]

class newform(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}), label="Description")
    bid = forms.FloatField(label="Bid", min_value=0)
    category = forms.CharField(label="Category", widget=forms.Select(choices=CATEGORY))
    image = forms.CharField(label="Image URL")

def index(request):
    return render(request, "auctions/index.html", {
        "listings": listings.objects.all()
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

@login_required
def create_listing(request):
    if request.method == "POST":
        #store everything in the model, including who created it.
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        category = request.POST["category"]
        image = request.POST["image"]
        listing = listings(user=request.user, title=title, description=description, bid=bid, category=category, image=image)
        listing.save()
        return HttpResponseRedirect(reverse("index"),{
            "listings": listings.objects.all()
        })
    return render(request, "auctions/create.html", {
        "form": newform()
    })

def show_listing(request, listings_id):
    list_id = listings.objects.get(pk=listings_id)
    if not request.user.is_authenticated:
        return render(request, "auctions/listing.html",{
        "listing": list_id,
        "comments": comments.objects.filter(listing=list_id)
        })
    return render(request, "auctions/listing.html",{
        "listing": list_id,
        "watchlist": watchlist.objects.filter(user=request.user),
        "bids": bids.objects.filter(listing=list_id).last(),
        "comments": comments.objects.filter(listing=list_id)
    })

@login_required
def watchlist_view(request):
    if request.method == "POST":
        subject = request.POST["name"]
        listingid = request.POST["listingid"]
        # mylist = list(watchlist.watching.get_queryset().values_list('id', flat=True))
        if subject == "add":
            #need to import IDs
            if watchlist.objects.filter(watching_id=listingid):
                return render(request, "auctions/listing.html",{
                "listing": listings.objects.get(pk=listingid),
                "message": "Already in Watchlist"
                })
            else:
                item = watchlist(user=request.user, watching=listings.objects.get(id=listingid))
                item.save()
        elif subject == "remove":
            item = watchlist.objects.filter(watching_id=listingid).delete()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist.objects.filter(user=request.user).order_by("watching")
    })

def bid(request):
    if request.method == "POST":
        bid_amount = float(request.POST["bid"])
        listingid = request.POST["listingid"]
        current_bid = listings.objects.filter(id=listingid)
        for c in current_bid:
            if bid_amount > c.bid:
                #replace bid else too low message
                listings.objects.filter(id=listingid).update(bid=bid_amount)
                item = bids(user=request.user, amount=bid_amount, listing=listings.objects.get(id=listingid))
                item.save()
                return render(request, "auctions/listing.html",{
                "listing": listings.objects.get(pk=listingid),
                "message": "You are now the highest bidder!"
                })
    return render(request, "auctions/listing.html",{
        "listing": listings.objects.get(pk=listingid),
        "message": "Amount too low!"
        })

@login_required
def close_listing(request):
    if request.method == "POST":
        status = request.POST["status"]
        listingid = request.POST["listingid"]
        listings.objects.filter(id=listingid).update(status=status)
        return render(request, "auctions/listing.html",{
        "listing": listings.objects.get(pk=listingid),
        "message": "Sold!"
        })

def make_comments(request):
    if request.method == "POST":
        comment = request.POST["comment"]
        listingid = request.POST["listingid"]
        new = comments(user=request.user, comment=comment, listing=listings.objects.get(id=listingid))
        new.save()
        return render(request, "auctions/listing.html",{
        "listing": listings.objects.get(pk=listingid),
        "comments": comments.objects.filter(listing=listingid),
        "message": "That a boy!"
        })

def categories(request):
    mylist = list(listings.objects.get_queryset().values_list('category', flat=True))
    new_list = []
    for item in mylist:
        if item not in new_list:
            new_list.append(item)
    return render(request, "auctions/categories.html", {
        "listings": listings.objects.all(),
        "categories": new_list
    })

def category_view(request, category):
    list_id = listings.objects.filter(category=category)
    return render(request, "auctions/category.html",{
    "listings": list_id,
    "category": category
    })