from django.db import models



from django.contrib.auth.models import User
# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=150)
    api_id = models.IntegerField()



class Profile(models.Model):
    display_name = models.CharField(max_length=50)
    movies_list = models.ManyToManyField(Movie)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.display_name


