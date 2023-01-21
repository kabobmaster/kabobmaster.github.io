from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from auctions.models import *

from .models import User

class newform(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}), label="Description")
    bid = forms.FloatField(label="Bid", min_value=0)
    category = forms.CharField(label="Category")
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
        listing = listings(title=title, description=description, bid=bid, category=category, image=image)
        listing.save()
        return HttpResponseRedirect(reverse("index"),{
            "listings": listings.objects.all()
        })
    return render(request, "auctions/create.html", {
        "form": newform(),
    })