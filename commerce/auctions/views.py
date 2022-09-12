from ast import Raise
from email.mime import image
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Listing, Bid, Comment

categories = ["Fashion", "Toys", "Electronics", "Home"]


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

@login_required(login_url="/login")
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        image = request.POST["image"]
        category = request.POST["category"]
        startingBid = request.POST["starting_bid"]
        description = request.POST["description"]

        new = Listing(title=title, creator=request.user, image=image, description=description, startingBid=startingBid, category=category)
        new.save()
        return redirect("index")
        
    return render(request, "auctions/create.html", {
        "categories": categories,
    })


def listing(request, id):
    try:
        listing = Listing.objects.get(pk=id)
        watchlist = listing.watchList.all()
        if request.method == "POST":
            if request.user not in watchlist:
                listing.watchList.add(request.user)
            else:
                listing.watchList.remove(request.user)
            return redirect(request.META['HTTP_REFERER'])
        return render(request, "auctions/listing.html", {
                "listing": listing,    
                "watchlist": watchlist,
                "comments": Comment.objects.filter(listing=listing)       
            })
    except ObjectDoesNotExist:  
        return render(request, "auctions/error.html", {
            "message": "This listing does not exist!"
        })
    
    
def bid(request, id):
    listing = Listing.objects.get(pk=id)
    if request.method == "POST":
        offer = request.POST["offer"]
        if offer:
            if (float(offer) < listing.startingBid):
                return render(request, "auctions/error.html", {
                    "message": "Your offer has to be bigger than the current bid.",
                    "app": "listing/" + id,
                })
            bid = Bid(bid=float(offer), user=request.user)
            bid.save()
            
            listing.bid = bid
            listing.save() 
        else:
            return render(request, "auctions/error.html",{
                "message": "Place your bid.",
                "app": "listing/" + id,
                
            })    
                
    return redirect("listing", id)

def close(request, id):
    listing = Listing.objects.get(pk=id)
    listing.isClosed = True    
    listing.save()
    return redirect("index")

def comment(request, id):
    listing = Listing.objects.get(pk=id)
    if request.method == "POST":
        comment = request.POST["comment"]
        addComment = Comment(comment=comment, user=request.user, listing=listing)
        addComment.save()
    return redirect("listing", id)

def watchlist(request, user_id):
    watching = request.user.listing_watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": watching
    })

def category(request):
    if request.method == "POST":
        category = request.POST["categories"]
        return render(request, "auctions/category.html", {
            "listings": Listing.objects.filter(category=category)
        })
        

    return render(request, "auctions/category.html", {
        "categories": categories
    })