from django import forms
from .models import Comment, Profile, User , Film



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('display_name', 'first_name', 'last_name')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields =('title',)
