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


class Event(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='school_events')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['event_date', 'event_time', 'title']

    def __str__(self):
        return f'{self.title} ({self.event_date})'

class GalleryImage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PortfolioWork(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(
        upload_to='portfolio/',
        blank=True,
        null=True
    )
    project_url = models.URLField(blank=True)
    project_file = models.FileField(
        upload_to='portfolio/files/',
        blank=True,
        null=True
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='portfolio_works'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Material(models.Model):
    MATERIAL_TYPES = [
        ('file', 'File'),
        ('image', 'Image'),
        ('link', 'Link'),
        ('youtube', 'YouTube Video'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    material_type = models.CharField(
        max_length=10,
        choices=MATERIAL_TYPES,
        default='file'
    )

    file = models.FileField(
        upload_to='materials/files/',
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='materials/images/',
        blank=True,
        null=True
    )

    url = models.URLField(blank=True)

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='materials'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
