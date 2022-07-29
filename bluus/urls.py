"""Defines URL patterns for bluus"""
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from . import views

app_name = 'bluus'

urlpatterns = [
    # News Feed
    path('', views.index, name='index'),
    # Page for adding a new post
    path('new_post/', views.new_post , name='new_post'),
    # Detail page for a single post and its comments '
    path('<int:post_id>/', views.post, name='post'),
    # Page for editing a post
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    # Page for editing a comment
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    #to like a post
    path('like_post', views.like, name='like'),
    #to view a user's profile page'
    path('profile/<int:user_id>/', views.profile, name='profile'),
    #to follow or unfollow a user
    path('follow', views.follow, name='follow'),
    #to see a user's full profile details
    path('profile_details/<int:user_id>/', views.profile_details, name='profile_details'),
    #edit profile
    path('edit_profile/<int:user_id>/',views.edit_profile, name='edit_profile'),
    #to delete a post
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    #to delete a comment
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    #to like a comment
    path('like_comment', views.like_comment, name='like_comment'),
    #display followers
    path('followers/<int:user_id>/', views.followers, name='followers'),
    #display followings
    path('following/<int:user_id>/', views.following, name='following'),
    #about bluu page
    path('about', views.about, name='about'),
    #search feature
    path('search/', views.search, name='search'),
    #chat
    path('chat/<int:user_id>/',views.chat,name='chat'),
    #list of chats a user is in
    path('chats',views.chats, name='chats'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#for saving the pics
