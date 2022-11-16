from time import time, timezone
from django.db import models

# Create your models here.
from django.utils import timezone

class Agegroup(models.Model):
    age_group = models.CharField(max_length=80)

class User(models.Model):
    username = models.CharField(max_length=80)
    password = models.CharField(max_length=80)
    age_group = models.ForeignKey(Agegroup, on_delete=models.CASCADE, null=True)
    mail = models.EmailField(default=None)

class Genres(models.Model):
    genre_name = models.CharField(max_length=80)

class Article(models.Model):
    headline = models.CharField(max_length=80)
    content = models.TextField(default="Error Content Missing")
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE, null=True)
    age_group = models.ForeignKey(Agegroup, on_delete=models.CASCADE, null=True)
    date_read= models.DateTimeField(auto_now_add=True, null=True)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)




