from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Advertisement(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='advertisement')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}, {self.text}, {self.creator}, {self.created_at}'


class GalleryImage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="gallery/")
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="gallery_images"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PortfolioWork(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="portfolio/", blank=True, null=True)
    project_url = models.URLField(blank=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="portfolio_works"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
