from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json
from .models import User,Posts,Follows
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
def index(request):
    return render(request, "network/index.html")
@csrf_exempt
@login_required
def set_posts(request):
      if request.method!="POST":
          return JsonResponse({"error": "POST request required."}, status=400)
      data=json.loads(request.body)
      print(f'{request.user}:{data.get("posts")}')
      posts=Posts(post=data.get("posts"),user=request.user)
      posts.save()
      return JsonResponse({"message": "Email sent successfully."}, status=201)
      
@csrf_exempt
@login_required
def get_posts(request,type):
    l=[]
    if type=="profile":
        l=User.objects.filter(username=request.user)
        return JsonResponse([i.serialize() for i in l],safe=False)
    elif type=="all_posts":
        print("all_posts")
        l=Posts.objects.all()
        l=sorted(l,key=lambda X:X.time_stamp,reverse=True)
        t=[]
        for i in l:
            if i.user.username!=request.user:
                t.append(i)
        return JsonResponse([i.serialize(request.user) for i in t],safe=False)
    elif type=="posts":
        followers=Follows.objects.filter(follower=request.user)
        for i in followers:
            obj=User.objects.get(username=i.user)
            post=Posts.objects.filter(user=obj)
            l+=post
        l=sorted(l,key=lambda x:x.time_stamp,reverse=True)
        return JsonResponse([i.serialize(id=request.user) for i in l],safe=False)
    elif type=="search_profile":
        if request.method!="POST":
          return JsonResponse({"error": "POST request required."}, status=400)
        else:
            data=json.loads(request.body)
            l=User.objects.filter(username=data.get("search_key"))
            print(l)
            return JsonResponse([i.serialize(request.user) for i in l],safe=False)
    elif type=="following":
        obj=Follows.objects.filter(follower=request.user)
        print([i.user.serialize() for i in obj])
        return JsonResponse([i.user.serialize(request.user) for i in obj],safe=False)
@csrf_exempt
def edit_post(request):
    if request.method!="POST":
        return JsonResponse({"message":"Invalid Operation"})
    else:
        data=json.loads(request.body)
        print(data.get("updated_post"))
        post_obj=Posts.objects.get(id=data.get("id"))
        post_obj.post=data.get("updated_post")
        post_obj.save()
        return JsonResponse({"message":f"Post Updated with {post_obj.post}"})

def get_user(request,username):
     
    obj=User.objects.get(id=username)
    print(obj)
    return JsonResponse([obj.serialize(request.user)],safe=False)

def get_user_posts(request,username):
    obj=User.objects.get(id=username)
    posts=Posts.objects.filter(user=obj.id)
    print(posts)
    return JsonResponse([i.serialize(request.user) for i in posts],safe=False)

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def follow(request,user_id,type):
    if(type=="follow"):
        obj1=User.objects.get(id=user_id)
        print(obj1.id)
        if len(Follows.objects.filter(user=obj1))==0:
            obj=Follows(user=obj1)
            obj.save()
            obj.follower.add(request.user)
            obj.save()
        else:
            obj=Follows.objects.get(user=obj1)
            obj.follower.add(request.user)
        return JsonResponse({"message": f"{obj1.username} was followed by {request.user}."}, status=201)
    elif(type=="Unfollow"):
         
        user_obj=get_object_or_404(User, username=request.user)
        post=Follows(user=user_id)
        post.follower.remove(user_obj)
         
        return JsonResponse({"message": f"{obj1.username} was unfollowed by {request.user}."}, status=201)

    

def like_post(request,post_id,type):
    if type=="like":
        obj=Posts.objects.get(id=post_id)
        obj.likes.add(request.user)
        obj.save()
        return JsonResponse({"message":f"{request.user} liked {post_id}"})
    elif type=="dislike":
        user_obj=get_object_or_404(User, username=request.user)
        post=Posts(id=post_id)
        post.likes.remove(user_obj)
        return JsonResponse({"message":f"{request.user} disliked {post_id}"})
    






def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
