from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=63)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topics")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.title

class Post(models.Model):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(
        upload_to="post_images/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
                return f"{self.author}, {self.topic}"