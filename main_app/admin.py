from django.contrib import admin

# Register your models here.
from .models import Profile, Photo, Comment, Film

admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(Comment)
admin.site.register(Film)
