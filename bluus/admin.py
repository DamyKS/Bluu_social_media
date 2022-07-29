from django.contrib import admin

from .models import Post, Comment, Profile, Chat, Message

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Chat)
admin.site.register(Message)