from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from commerce.forms import New_listing
from .models import Localuser,listings
from datetime import datetime 


def index(request):
    model=listings.objects.all()
    return render(request, "auctions/index.html",{"model":model,"now":datetime.now().date()})


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

def create_listing(request):
     
    if request.method=="POST":
         form=New_listing(request.POST or None)
         if form.is_valid():
            title=form.cleaned_data["title"]
            description=form.cleaned_data["description"]
            bid_price=form.cleaned_data["bid_price"]
            end_date=form.cleaned_data["end_date"]
            category=form.cleaned_data["category"]
            model=listings(item_name=title,item_description=description,bid_price=bid_price,end_date=end_date,category=category)
            model.save()
            return render(request,"auctions/new_listing.html",{"form":New_listing()})              

    return render(request,"auctions/new_listing.html",{"form":New_listing()})

def listing(request,name):
    item=listings.objects.get(item_name=name)
    return render(request,"auctions/listing.html",{"item":item})
    