from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Film(models.Model):
    title = models.CharField(max_length=150)

    
    def __str__(self):
        return self.name

class Profile(models.Model):
    display_name = models.CharField(max_length=50)
    films_list = models.ManyToManyField(Film)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # added the use foriegn key

    def __str__(self):
        return self.display_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Comment(models.Model):
    film = models.CharField(max_length=200)
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