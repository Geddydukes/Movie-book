from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Photo, Movie, Profile, Comment
import uuid
import boto3
from .forms import CommentForm



S3_BASE_URL = 'https://s3.dualstack.us-west-1.amazonaws.com/'
BUCKET = 'movie-book-profiles'
# Create your views here.

def home(request):
    return render(request, 'home.html')

def profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    return render(request , 'profile/index.html', {'profile': profile})


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)





# logic for uploading photos to AWS S3
def add_photo(request, profile_id):
    photo_file = request.FILES.get('photo-file', None)
    print(photo_file)
    if photo_file:
        s3 = boto3.client('s3')
        print(s3)
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        print(key)
        try: 
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            print(url)
            photo = Photo(url=url, profile_id=profile_id)
            photo.save()
        except:
            print('An error occured uploading file to S3')
    return redirect('profile', profile_id=profile_id)




def add_comment_to_movie(request, api_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.api_id = api_id
        new_comment.save()
        return redirect('profile', api_id=api_id)



def edit_profile(request, profile_id):
  profile = Profile.objects.get(id=profile_id)
  if request.method == 'POST':
    form =         