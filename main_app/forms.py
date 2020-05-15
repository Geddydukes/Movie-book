from django import forms
from .models import Comment, Profile



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('display_name', 'email', 'first_name', 'last_name')