from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
import json
from django.core.paginator import Paginator
import jsonpickle
from json import JSONEncoder
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .forms import PostForm

from .models import User, Post


# index view function
@login_required(redirect_field_name='login')
def index(request):
    user = request.user
    postmod = Post.objects.all()
    orderedposts = postmod.order_by("-time").all()
    paginator = Paginator(orderedposts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        "posts": page_obj})


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
        bio = request.POST["bio"]
        avatar_url = request.POST["avatar"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User(username=username, email=email, password=make_password(password), avatar_url=avatar_url, bio=bio)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
    
    
    
    
 # function to create a new post GET & POST
@login_required(redirect_field_name='login')
def new_post(request):
    
    posts = PostForm(request.POST)
    
    if request.method == "POST":
        p = posts.save(commit=False)
        p.author = request.user
        p.save()
        postmod = Post.objects.all()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/newpost.html",{
            "postform": posts
        })
        
        
        
        
        
# function to view post
@csrf_exempt
def view_post(request,id):
    
     # Query for requested post
    try:
        post = Post.objects.get(pk=id)
        if request.method == "PUT":
            data = json.loads(request.body)
            
            # check for edited post
            if data.get("post"):
                post.post = data['post']
                post.save()
                
                # check for liked/unliked post
            if data.get("liked_by") == 'true':
                post.liked_by.add(request.user)
            else:
                post.liked_by.remove(request.user)
                post.save()
            return HttpResponse(status=204)
        
        #return json for post model
        elif request.method == "GET":
            return JsonResponse(jsonpickle.encode(post.post), safe=False)
    except Post.DoesNotExist:
        return JsonResponse({"error": "This Post Doesn't seem to exist."}, status=404)


 # function to view user profile       
@login_required(redirect_field_name='login')
def profile(request,id):
    model = User.objects.get(pk = id)
    user = request.user
    following = False
    follow = model.followers.all()
    for f in follow:
        if user == f:
            following = True
    ownposts = Post.objects.order_by("-time").filter(author = model)
    paginator = Paginator(ownposts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "following": following,
        "model": model,
        "posts": page_obj})
    
    
    
    
 # function to follow another user   
@login_required(redirect_field_name='login')
def addfollower(request,id):
    model = User.objects.get(pk=id)
    current = User.objects.get(pk=request.user.id)
    model.followers.add(current)
    model.save()
    current.following.add(model)
    current.save()
    return HttpResponseRedirect(reverse("profile", args=(id,)))

   
    
  
  # remove follower /unfollow  
@login_required(redirect_field_name='login')
def unfollow(request,id):
    model = User.objects.get(pk=id)
    current = User.objects.get(pk=request.user.id)
    model.followers.remove(current)
    model.save()
    current.following.remove(model)
    current.save()
    return HttpResponseRedirect(reverse("profile", args=(id,)))




def following_posts(request):
    current =  User.objects.get(pk=request.user.id)
    following = current.following.all()
    followposts = Post.objects.filter(author__in = following)
    orderedposts = followposts.order_by("-time").all()
    paginator = Paginator(orderedposts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html",{
        "posts": page_obj})
    


    