from django.contrib import admin
from .models import Post, PostImage, Like, Comment

admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Like)
admin.site.register(Comment)