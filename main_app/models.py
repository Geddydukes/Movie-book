from django.db import models
from django.utils import timezone


from django.contrib.auth.models import User
# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=150)
    api_id = models.IntegerField()
    def __str__(self):
        return self.name


class Profile(models.Model):
    display_name = models.CharField(max_length=50)
    movies_list = models.ManyToManyField(Movie)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    def __str__(self):
        return self.display_name


class Comment(models.Model):
    movie = models.IntegerField() 
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class Photo(models.Model):
    url = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for profile_id: {self.profile_id} @{self.url}"