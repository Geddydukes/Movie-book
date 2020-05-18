from django import forms
from .models import Comment, Profile
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User





class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('display_name', 'email', 'first_name', 'last_name')


class RegisterForm(UserCreationForm):  
   email = forms.EmailField()

   class Meta:
     model = User
     fields = ["username", "email", "password1", "password2"]  

