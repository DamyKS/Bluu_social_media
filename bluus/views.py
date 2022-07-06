from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.db.models import Q

from .models import Post, Comment, Profile
from .forms import PostForm, CommentForm, ProfileForm

def index(request):
    """Show the newsfeed and display all posts"""
    posts = Post.objects.order_by('-date_added')
    profiles=Profile.objects.all()
    context = {'posts': posts,'profiles': profiles}
    return render(request, 'bluus/index.html', context)

@login_required
def new_post(request):
    """Add a new post."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = PostForm()
    else:
        # POST data submitted; process data.
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            if new_post.caption=="" and new_post.pic == None:
                return redirect(request.path)
            else:              
                new_post.owner = request.user
                new_post.save()
                return redirect('bluus:index')
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'bluus/new_post.html', context)  

def post(request, post_id):
    """Show a single post and all its comments."""
    #Get the post and all its comments 
    post=get_object_or_404(Post, id=post_id)
    profiles=Profile.objects.all()
    comments = post.comment_set.order_by('-date_added')
    
    # A form to add comments
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = CommentForm()
    else:
        # POST data submitted; process data.
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment= form.save(commit=False)
            new_comment.post=post
            new_comment.owner=request.user
            new_comment.save()
            return redirect(request.path)
            
        
    
    context={'post':post,'comments': comments, 'form': form, 'profiles': profiles}
    return render(request, 'bluus/post.html', context)
    
@login_required
def edit_post(request, post_id):
    """Edit an existing post."""

    post = get_object_or_404(Post, id=post_id)
    #check if the user trying to edit owns the post
    if post.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # Initial request; pre-fill form with the current post
        form = PostForm(instance=post)
    else:
        # POST data submitted; process data.
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bluus:index')
    
    context = {'post':post, 'form': form}
    return render(request, 'bluus/edit_post.html', context)

@login_required
def delete_post(request, post_id):
    """a view that deletes a particular post"""
    post = get_object_or_404(Post, id=post_id)
    #check if the user trying to edit owns the post
    if post.owner != request.user:
        raise Http404
    #delete the post
    post.delete()
    
    return redirect('bluus:index')
    
    
@login_required
def edit_comment(request, comment_id):
    """Edit an existing comment."""

    comment = Comment.objects.get(id=comment_id)
    #check if the iser owns the comment before editing
    if comment.owner != request.user:
        raise Http404
    post= comment.post
    
    if request.method != 'POST':
        # Initial request; pre-fill form with the current post
        form = CommentForm(instance=comment)
    else:
        # POST data submitted; process data.
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bluus:post', post_id=post.id)
    
    context = {'comment':comment, 'post':post, 'form': form}
    return render(request, 'bluus/edit_comment.html', context)

@login_required
def delete_comment(request, comment_id):
    """a view that deletes a particular comment"""
    comment = Comment.objects.get(id=comment_id)
    #get the post associated with the comment so you can redirect to it later 
    post=comment.post
    
    #check if the user trying to edit owns the commemt
    if comment.owner != request.user:
        raise Http404
        
    #delete the comment
    comment.delete()
    
    return redirect('bluus:post', post_id=post.id)
    
    
@login_required
def like(request, post_id):
    """like an existing ppst"""
    post=Post.objects.get(id=post_id)
    
    is_liked=False
    for person in post.liked_by.all():
        if person == request.user:
            is_liked=True
            break
    
    if is_liked==False:
        post.liked_by.add(request.user)
    if is_liked==True:
        post.liked_by.remove(request.user)
    post.num_of_likes=post.liked_by.count()
    post.save()
    
    return redirect('bluus:index')

@login_required
def like_comment(request, comment_id):
    """like an existing comment"""
    comment=Comment.objects.get(id=comment_id)
    
    is_liked=False
    for person in comment.liked_by.all():
        if person == request.user:
            is_liked=True
            break
    
    if is_liked==False:
        comment.liked_by.add(request.user)
    if is_liked==True:
        comment.liked_by.remove(request.user)
        
    comment.save()
    post=comment.post
    
    return redirect('bluus:post', post_id=post.id)
    
def profile(request, user_id):
    """show a user's profile page"""
    #get the users details 
    user=User.objects.get(id=user_id)
    user_profile=Profile.objects.get(id=user_id)
    profiles=Profile.objects.all()
    user_posts=user.post_set.order_by('-date_added')
    
    context={'user':user ,'user_profile':user_profile, 'user_posts': user_posts, 'profiles': profiles}   
    return render(request,'bluus/profile.html', context)

def followers(request, user_id):
    """to see the list of people that follows a user"""
    user=User.objects.get(id=user_id)
    user_profile=Profile.objects.get(id=user_id)
    followers=user_profile.followers.all()
    profiles=Profile.objects.all()
    
    context={'followers':followers, 'profiles':profiles, 'user': user}
    
    return render(request, 'bluus/followers.html', context)

def following(request, user_id):
    """To display the users that a user follows """
    user=User.objects.get(id=user_id)
    following=user.follows.all()
    profiles=Profile.objects.all()
    
    context={'following':following, 'profiles':profiles, 'user': user}
    
    return render(request, 'bluus/following.html', context)
    
  
      
@login_required
def follow(request, user_id):
    """allow a user to follow or unfollow another user"""
    #get the specific  profile
    profile=Profile.objects.get(id=user_id)
    if request.user==profile.owner:
        return redirect('bluus:profile',user_id)
    else:        
        followed=False
        for person in profile.followers.all():
            if person==request.user:
                followed=True
                break
        if followed==False:
            profile.followers.add(request.user)
        if followed==True:
            profile.followers.remove(request.user)
            
        profile.save()
        return redirect('bluus:profile',user_id)

def profile_details(request,user_id):
    """To show the full details of a user's profile"""
    user=User.objects.get(id=user_id)
    user_profile=Profile.objects.get(id=user_id)
    
    context={'user':user ,'user_profile':user_profile}   
    return render(request,'bluus/profile_details.html', context)

@login_required
def edit_profile(request, user_id):
    """to edit some of the profile details of a user"""
    #get the prpfile 
    user_profile=Profile.objects.get(id=user_id)
    #check if it's the owner that wants to make the changes
    if user_profile.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # Initial request; pre-fill form with the current post
        form = ProfileForm(instance=user_profile)
    else:
        # POST data submitted; process data.
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('bluus:profile' , user_id)
    
    context = {'user_profile': user_profile, 'form': form}
    return render(request, 'bluus/edit_profile.html', context)
    
def about(request):
    """to show the about bluu page"""
    return render(request, 'bluus/about.html' )

def search(request):
    """to filter profiles  and return a search result"""
    query = request.GET.get("q")
    search_profiles=Profile.objects.filter( Q(owner__username__icontains=query.replace(" ", "")
        ))
    
    search_posts=Post.objects.filter( Q(caption__icontains=query))
    
    profiles=Profile.objects.all()
    
    
    context={'search_profiles': search_profiles, 'search_posts': search_posts, 'profiles': profiles}
    
    return render(request, 'bluus/search.html', context)