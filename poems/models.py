from django.db import models
from django.contrib.auth.models import User


class Poem(models.Model):
    name = models.CharField(
        max_length=250,
    )
    text = models.CharField(
        max_length=10000,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.CharField(max_length=10000)
    poem = models.ManyToManyField(
        "Poem",
        related_name="review",
        null=True
    )
    author_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.text[:10]
