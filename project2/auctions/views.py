from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions.forms import New_listing,Edit_form
from .models import Localuser,Listings,Watchlist,Bid,Comments
from datetime import datetime 
from django.db.models import F
from django.contrib import messages
from .models import CATEGORIES
def index(request):
    model=Listings.objects.all()
    return render(request, "auctions/index.html",{"model":model,"now":datetime.now().date(),"user":request.user})


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
            user = Localuser.objects.create_user(username, email, password)
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
     
    if request.method=="POST":
         form=New_listing(request.POST or None)
         if form.is_valid():
            title=form.cleaned_data["title"]
            description=form.cleaned_data["description"]
            bid_price=form.cleaned_data["bid_price"]
            end_date=form.cleaned_data["end_date"]
            category=form.cleaned_data["category"]
            img_url=form.cleaned_data["image"]
            model=Listings(item_name=title,item_description=description,bid_price=bid_price,end_date=end_date,category=category,created_by=request.user,img_url=img_url)
            model.save()
            return render(request,"auctions/new_listing.html",{"form":New_listing(),"user":request.user})              

    return render(request,"auctions/new_listing.html",{"form":New_listing()})

def listing(request,name):
    item=Listings.objects.get(item_name=name)
    if Bid.objects.filter(list_item=item.id,bid_price=item.current_price).exists():
        highest_bidder=Bid.objects.get(list_item=item.id,bid_price=item.current_price)
    else:
        highest_bidder=None
    if Bid.objects.filter(user=request.user.id,list_item=item.id).exists():
        user_bid=Bid.objects.get(user=request.user.id,list_item=item.id)
    else:
        user_bid=None
    item_obj=Comments.objects.filter(item=item)
    return render(request,"auctions/listing.html",{"item":item,"user_bid":user_bid,"highest_bid":highest_bidder,"comments":item_obj})
    
@login_required
def watchlist(request):
     if request.method=="POST":
         item_name=request.POST.get("addtowatchlist")
          
         if not Watchlist.objects.filter(user=request.user,item=item_name).exists():
            item=request.POST.get("addtowatchlist")
            item=Listings.objects.get(id=item)
            model=Watchlist(item=item,user=request.user)
            model.save()
         else:
             item=Watchlist.objects.filter(user=request.user,item=item_name)
             item.update(count=F("count")+1)
      
     item=Watchlist.objects.filter(user=request.user)
     return render(request,"auctions/watchlist.html",{"item":item})

def remove_from_watchlist(request):
    if request.method=="POST":
        X=request.POST.get("removefromwatchlist")
        print(X)
        removed_item=Listings.objects.get(item=X)
        Watchlist.objects.filter(id=X).delete()
    return HttpResponseRedirect(reverse("watchlist"))
        
      
@login_required
def personal_listing(request):
    personal=Listings.objects.filter(created_by=request.user)
     
    return render(request,"auctions/personal_listing.html",{"personal":personal})


def edit(request):
    
    if request.method=="POST":
        item=request.POST.get("edit")
        item_obj=Listings.objects.get(item_name=item)
         
    return render(request,"auctions/edit.html",{"Form":Edit_form(),"item":item_obj})

def commit_bid(request):
    if request.method=="POST":
        print("entered")
        bid_price=request.POST.get("save_bid")
        item=request.POST.get("item")
        obj=Listings.objects.get(item_name=item)
        print(obj.item_name)
        if obj.current_price<float(bid_price):
            obj1=Listings.objects.filter(item_name=item)
            obj1.update(current_price=float(bid_price))
            if not Bid.objects.filter(user=request.user,list_item=obj).exists():
                model=Bid(user=request.user,list_item=obj,bid_price=float(bid_price))
                model.save()
            
            else:
                model=Bid.objects.filter(user=request.user,list_item=obj)
                model.update(bid_price=float(bid_price))
        else:
            messages.error(request,"Sorry!! Bid should be higher than current bid")
        
    return HttpResponseRedirect(reverse("listing",kwargs={"name":item}))


def comments(request):
     
    if request.method=="POST":
      
     item=request.POST.get("item")
     item=Listings.objects.get(id=item)
     comment=request.POST.get("comment")
     model=Comments(user=request.user,item=item,comments=comment)
     model.save()
    
    
    return HttpResponseRedirect(reverse("listing",kwargs={"name":item.item_name}))

def categories(request):
        l=[]
        for i in CATEGORIES:
            l.append(i[1])
        return render(request,"auctions/categories.html",{"category":l})