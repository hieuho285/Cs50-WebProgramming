import json
from pickle import TRUE

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from .models import User, Posts, Comments, Followers

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

def index(request):
    return render(request, "network/index.html")

@csrf_exempt
@login_required
def new_post(request):
    if request.method == "POST":
        body = json.loads(request.body).get("body", "")
        newPost = Posts(
            creator = request.user, 
            body = body,
        )
        newPost.save()
        return JsonResponse({"Message":"Posted"}, status=201)

def showallpost(request):
    posts = Posts.objects.all().order_by("-timestamp").all()


    return JsonResponse([post.serialize() for post in posts], safe=False)

@login_required
def showprofile(request, user):
    posts = Posts.objects.filter(creator=user).order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

@login_required
def follow(request, user):
    try:
        follower = Followers.objects.get(user=User.objects.get(username=user)).follower.all().count()
    except ObjectDoesNotExist:
        follower = 0
    try:
        following = User.objects.get(username=user).following.all().count()
    except ObjectDoesNotExist:
        pass
    
    if request.user in Followers.objects.get(user=User.objects.get(username=user)).follower.all():
        button = "Unfollow"
    else: 
        button = "Follow"
    return JsonResponse({"follower": follower, "following": following, "follow": button})


@login_required
def updatelike(request, post_id):
    post = Posts.objects.get(pk=post_id)
    if request.user not in post.users.all():
        post.users.add(request.user)
        post.save()
    else:
        post.users.remove(request.user)
        post.save()

    if request.user in post.users.all():
        button = "Unlike"
    else:
        button = "Like"

    return JsonResponse(post.serialize())

@login_required
def updatefollow(request, user):
    try:
        profile = Followers.objects.get(user=User.objects.get(username=user))
    except ObjectDoesNotExist:
        profile = Followers(user=User.objects.get(username=user))
        profile.save()
        
    if request.user in profile.follower.all():
        profile.follower.remove(request.user)
        profile.save()
    else:
        profile.follower.add(request.user)
        profile.save()

    return redirect("follow", user=user)

@login_required
def following(request, user):
    users = User.objects.get(username=user).following.all()
    allPosts = []
    for eachUser in users:
        posts = Posts.objects.filter(creator=eachUser.user.username).all()
        for post in posts:
            allPosts.append(post.serialize())

    return JsonResponse(allPosts, safe=False)   

def paginator(request):
    pass

