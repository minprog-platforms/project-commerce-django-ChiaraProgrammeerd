from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# from django.utils.datastructures import MultiValueDictKeyError

from .models import User, AuctionListing, Bid, Comment


def index(request):
    isActive = AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listing": isActive
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


def createlisting(request):
    if request.method == "GET":
        return render(request, "auctions/createlisting.html")

    if request.method == "POST":
        object = request.POST['object']
        price = request.POST['price']
        givedescription = request.POST['givedescription']
        objectimage = request.POST['objectimage']
        user = request.user
        bid = Bid(bid=float(price), bidder=user)
        bid.save()
        user = request.user
        auction = AuctionListing(
            title = object,
            price = bid,
            description = givedescription,
            image = objectimage,
            owner = user
        )
        auction.save()
        return HttpResponseRedirect(reverse("index"))

def listing(request, title):
    listing_information= AuctionListing.objects.get(title=title)
    listing_in_watchlist = request.user in listing_information.watchlist.all()
    comments = Comment.objects.filter(listing=listing_information)
    owner = request.user.username == listing_information.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listing_information,
        "listing_in_watchlist": listing_in_watchlist,
        "comments": comments,
        "owner": owner
    })

def remove(request, title):
    listing_information = AuctionListing.objects.get(title=title)
    user = request.user
    listing_information.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing",args=(title, )))


def add(request, title):
    listing_information = AuctionListing.objects.get(title=title)
    user = request.user
    listing_information.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing",args=(title, )))

def watchlist(request):
    user = request.user
    listings = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listing": listings
    })

def comment(request, title):
    user = request.user
    listing_information = AuctionListing.objects.get(title=title)
    comment = request.POST['comment']

    new_comment = Comment(
        commenter = user,
        listing = listing_information,
        comment = comment
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("listing",args=(title, )))

def bid(request, title):
    listing_information = AuctionListing.objects.get(title=title)
    new_bid = 'new_bid' in request.POST
    new_bid = request.POST['new_bid']
    user=request.user
    listing_in_watchlist = request.user in listing_information.watchlist.all()
    comments = Comment.objects.filter(listing=listing_information)
    if float(new_bid) > listing_information.price.bid:
        highest_bid = Bid(bid=float(new_bid), bidder=user)
        highest_bid.save()
        listing_information.price = highest_bid
        listing_information.save()
        return render(request, "auctions/listing.html", {
            "listing": listing_information,
            "listing_in_watchlist": listing_in_watchlist,
            "comments": comments,
            "message": "Highest bid!",
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing_information,
            "listing_in_watchlist": listing_in_watchlist,
            "comments": comments,
            "message": "There is a higher bid already! Couldn't update bid",
        })

def close(request, title):
    listing_information = AuctionListing.objects.get(title=title)
    listing_information.active = False
    listing_information.save()
    listing_in_watchlist = request.user in listing_information.watchlist.all()
    comments = Comment.objects.filter(listing=listing_information)
    owner = request.user.username == listing_information.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listing_information,
        "listing_in_watchlist": listing_in_watchlist,
        "comments": comments,
        "message": "Listing is closed!",
    })
