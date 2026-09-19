from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Choice(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    text = models.CharField(max_length=200)
    votes = models.ManyToManyField(
        User,
        blank=True,
        related_name='poll_votes'
    )

    def __str__(self):
        return self.text