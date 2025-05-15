from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Community, Subrabble, Post
from .forms import PostForm
from django.shortcuts import redirect
def index(request):
    subrabbles = Community.objects.get(community_name="default").subrabble_set.all()
    return render(request, "rabble/index.html", {"subrabbles": subrabbles})

def subrabble_detail(request, identifier):
    subrabble = get_object_or_404(Subrabble, identifier=identifier)
    posts = subrabble.post_set.all()
    return render(request, "rabble/subrabble_detail.html", {"subrabble": subrabble, "posts": posts})

def post_detail(request, identifier, pk):
    subrabble = get_object_or_404(Subrabble, identifier=identifier)
    post = Post.objects.get(pk=pk)
    return render(request, "rabble/post_detail.html", {"subrabble": subrabble, "post": post})

def post_create(request, identifier):
    subrabble = get_object_or_404(Subrabble, identifier=identifier)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.subrabble = subrabble
            form.save()
            return redirect("subrabble-detail", identifier=identifier)
    else:
        form = PostForm()
    return render(request, "rabble/post_form.html", {"subrabble": subrabble, "form": form})

def post_edit(request, identifier, pk):
    subrabble = get_object_or_404(Subrabble, identifier=identifier)
    post = get_object_or_404(Post, pk=pk)
    # not owner of the post!
    if post.user != request.user:
        return redirect("post-detail", identifier=identifier, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post-detail", identifier=identifier, pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, "rabble/post_form.html", {"subrabble": subrabble, "form": form})

def profile(request):
    return render(request, "rabble/profile.html")