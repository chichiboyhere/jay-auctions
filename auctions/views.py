from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import (
   Paginator, EmptyPage,
   PageNotAnInteger
)

from .models import *

# This is the default view
def index(request):
    # List of products available and order them from the most recently posted to the earliest
    listings = Listing.objects.all().order_by('-created_at')
    # Add paginator
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
   
    return render(request, "auctions/index.html", {
        "listings":listings,
        "posts": posts,
        "page":page
    })

def viewlisting(request, product_id):
    comments = Comment.objects.filter(listing_id=product_id)
    product = Listing.objects.get(id=product_id)
    categories = Listing.objects.filter(category=product.category).exclude(id=product.id)
    print(categories)
    # 'Post' method
    if request.method == "POST":
        item = Listing.objects.get(id=product_id)
        try:
            newbid = int(request.POST.get('newbid'))
        except ValueError:
            return render(request, "auctions/viewlisting.html", {
                "product": product,
                "message": "Wrong data form. Enter a number as your bid.",
                "msg_type": "danger",
                "comments": comments
            })
        # checking if the new bid is greater than or equal to current bid
        if item.starting_bid >= newbid:
            return render(request, "auctions/viewlisting.html", {
                "product": product,
                "message": "Your Bid should be higher than the Current one.",
                "msg_type": "danger",
                "comments": comments
            })
        # if bid is greater then we update the Listing table
        else:
            item.starting_bid = newbid
            item.save()
            # fetch the new bid
            bid_object = Bid.objects.filter(listing_id=product_id)
            if bid_object:
                # Delete the existing bid
                bid_object.delete()
            bidder = Bid()
            bidder.user = request.user.username
            bidder.title = item.title
            bidder.listing_id = product_id
            bidder.bid = newbid
            bidder.save()
            product = Listing.objects.get(id=product_id)
            return render(request, "auctions/viewlisting.html", {
                "product": product,
                "message": "Your bid is added. Keep your fingers crossed, hopefully you are the highest bidder.",
                "msg_type": "success",
                "comments": comments
            })
    # 'GET' method for the given product
    else:
        product = Listing.objects.get(id=product_id)
        added = Watchlist.objects.filter(listing_id=product_id, user=request.user.username)
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "added": added,
            "comments": comments,
            "categories": categories
        })
# This is the view for 'about us'
def aboutus(request):
    return render(request, "auctions/aboutus.html")


# This is the view for login
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
        # if not authenticated
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                "msg_type": "danger"
            })
    # if GET request
    else:
        return render(request, "auctions/login.html")


# view for logging out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# view for registering
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                "msg_type": "danger"
            })
        if not username:
            return render(request, "auctions/register.html", {
                "message": "Please enter your username.",
                "msg_type": "danger"
            })
        if not email:
            return render(request, "auctions/register.html", {
                "message": "Please enter your email.",
                "msg_type": "danger"
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "msg_type": "danger"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    # if GET request
    else:
        return render(request, "auctions/register.html")
    
#view for contact
def contact_us (request):
    listings = Listing.objects.all().order_by('-created_at')
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    if request.user.is_authenticated:
        name= request.user.username
        email= request.user.email
        message = request.POST["message"]
    else:
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]
    ContactMessage.objects.create(
          name=name,
          email=email,
          message=message,
    )
    return render(request, "auctions/index.html",{
                "message": "Your message was received. Thanks.",
                "msg_type": "success",
                "posts": posts,
                "page":page,
                "listings": listings
            }) 
    # return render(request, "auctions/index.html", {
    #             "message": "Your message was received. Thanks.",
    #             "msg_type": "success"
    #         })
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     name = customer.name
    #     email = customer.email
    #     subject = data['form']['subject']
    #     message = data['form']['message']
    # else:
    #     name = data['form']['name']
    #     email = data['form']['email']
    #     subject = data['form']['subject']
    #     message = data['form']['message']
    # ContactMessage.objects.create(
    #       name=name,
    #       email=email,
    #       subject=subject,
    #       message=message
    # )

# view for dashboard
@login_required(login_url='/login')
def dashboard(request):
    # Fetch the stats of the logged in bid winner 
    winnings = Winner.objects.filter(winner=request.user.username)
    # Fetch all the items in a user's watchlist
    watch_list = Watchlist.objects.filter(user=request.user.username)
    # List of products available in WinnerModel
    present = False
    # Product list created and initialized to an empty list
    product_list = []
    if watch_list:
        present = True
        for item in watch_list:
            # Get every product in the user's watchlist whose listing_id is an active listing 
            product = Listing.objects.get(id=item.listing_id)
            # Add the product to the product list created
            product_list.append(product)
    return render(request, "auctions/dashboard.html", {
        "product_list": product_list,
        "present": present,
        "winnings": winnings
    })
  
# view to create a lisiting
@login_required(login_url='/login')
def createlisting(request):
    # If user submitted the create listing form
    if request.method == "POST":
        # Item is of type Listing (object)
        item = Listing()
        # Assigning the data submitted via form to the object
        item.seller = request.user.username
        item.title = request.POST.get('title')
        item.description = request.POST.get('description')
        item.category = request.POST.get('category')
        item.image = request.FILES.get('image')
        try:
            item.starting_bid = request.POST.get('starting_bid')
            item.save()
        except ValueError:
            return render(request, "auctions/createlisting.html", {
                "message": "Wrong data form. Enter a number as your bid.",
                "msg_type": "danger"
            })
        # Let the user know his listing was successfully created
        return render(request, "auctions/createlisting.html", {
                "message": "Your Listing was successfully created. Visit the index page to view it",
                "msg_type": "success",
            })
    # For a 'GET' request:
    else:
        return render(request, "auctions/createlisting.html")


# view to display all the categories
@login_required(login_url='/login')
def categories(request):
    return render(request, "auctions/categories.html")

# view to display all the active listings in that category
@login_required(login_url='/login')
def category(request, name):
    # retieving all the products that fall into this category
    listings = Listing.objects.filter(category=name)
    # empty = False
    # if len(listings) == 0:
    #     empty = True
    return render(request, "auctions/category.html", {
        "name": name,
        # "empty": empty,
        "listings": listings
    })


# View to add or remove products to watchlists
@login_required(login_url='/login')
def addtowatchlist(request, product_id):

    item = Watchlist.objects.filter(
        listing_id=product_id, user=request.user.username)
    comments = Comment.objects.filter(listing_id=product_id)
    # Checking if it is already added to the watchlist
    if item:
        # Its already there then user wants to remove it from watchlist
        item.delete()
        # Returning the updated content
        product = Listing.objects.get(id=product_id)
        added = Watchlist.objects.filter(
            listing_id=product_id, user=request.user.username)
        print(added)
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "added": added,
            "comments": comments
        })
    else:
        # If it not present then the user wants to add it to watchlist
        item = Watchlist()
        item.user = request.user.username
        item.listing_id = product_id
        item.save()
        # Returning the updated content
        product = Listing.objects.get(id=product_id)
        added = Watchlist.objects.filter(
            listing_id=product_id, user=request.user.username)
        print(added)
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "added": added,
            "comments": comments
        })


# view for comments
@login_required(login_url='/login')
def addcomment(request, product_id):
    comment = Comment()
    comment.text = request.POST.get("comment")
    comment.user = request.user.username
    comment.listing_id = product_id
    comment.save()
    comments = Comment.objects.filter(listing_id=product_id)
    product = Listing.objects.get(id=product_id)
    added = Watchlist.objects.filter(
        listing_id=product_id, user=request.user.username)
    return render(request, "auctions/viewlisting.html", {
        "product": product,
        "added": added,
        "comments": comments
    })


# view when the user wants to close the bid
@login_required(login_url='/login')
def closebid(request, product_id):
    # Fetch winner of listed item
    item_winner = Winner()
    # Fetch the listing whose id matches the given product to be closed
    listed_obj = Listing.objects.get(id=product_id)
    # Try to fetch the bids placed on this product we're about to close
    try:
        obj = Bid.objects.get(listing_id=product_id)
    except Bid.DoesNotExist:
        obj = None
    
    
    if obj==None:
        message = "Deleting Bid"
        msg_type = "danger"
    else:
        bid_object = Bid.objects.get(listing_id=product_id)
        # Store the seller of the listing as the user requesting a closed bid
        item_winner.owner = request.user.username
        # Store the winner of the bid as the user with the current highest bid
        item_winner.winner = bid_object.user
        # Store additional info about the given listing: its 'id', 'highest bid placed' and 'title'
        item_winner.listing_id = product_id
        item_winner.winprice = bid_object.bid
        item_winner.title = bid_object.title
        # Saved the closed listing
        item_winner.save()
        message = "Bid Closed"
        msg_type = "success"
        # Remove the closed listing from Bid
        bid_object.delete()
    # Remove closed listing from watchlist if one exists
    if Watchlist.objects.filter(listing_id=product_id):
        watchlist_obj = Watchlist.objects.filter(listing_id=product_id)
        watchlist_obj.delete()
    # Remove closed listing from Comment
    if Comment.objects.filter(listing_id=product_id):
        comment = Comment.objects.filter(listing_id=product_id)
        comment.delete()
    # Removing it from Listing
    listed_obj.delete()
    # Retrieving the winners from the Winners' table and ordering them from the latest to the earliest winner
    winners = Winner.objects.all().order_by('-id')
    # Checking if there are any winners
    empty = False
    if len(winners) == 0:
        empty = True
    return render(request, "auctions/closedlisting.html", {
        "products": winners,
        "empty": empty,
        "message": message,
        "msg_type": msg_type
    })


# view to see closed listings
@login_required(login_url='/login')
def closedlisting(request):
    # Retrieving the winners from the Winners' table and ordering them from the last to the earliest winner
    winners = Winner.objects.all().order_by('-id')
    # checking if there are any products
    empty = False
    if len(winners) == 0:
        empty = True
    return render(request, "auctions/closedlisting.html", {
        "products": winners,
        "empty": empty
    })


    
