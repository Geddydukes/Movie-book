from django import forms
from .models import Comment, Profile, User



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('display_name', )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')




