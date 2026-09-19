from django.contrib import admin
from .models import Category, Topic, Post
# Register your models here.
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Category)