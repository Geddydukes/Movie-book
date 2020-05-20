from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Photo, Film, Profile, Comment 
from django.contrib.auth.models import User


import uuid
import boto3
from .forms import CommentForm, ProfileForm , UserForm ,FilmForm

from tmdbv3api import TMDb, Movie, TV
tmdb = TMDb()
tmdb.api_key = '5cc2c3fe2401b50f702a6631a34199d2'
tmdb.language = 'en'
tmdb.debug = True



S3_BASE_URL = 'https://s3.dualstack.us-west-1.amazonaws.com/'
BUCKET = 'movie-book-profiles'


def home(request):
    return render(request, 'home.html')


def profile(request, profile_id):
    profile = User.objects.get(id=profile_id)

    return render(request , 'profile/index.html', {'profile': profile})


def about_us(request):
    return render(request, 'about.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            return redirect(f'/accounts/profile/{user.id}/edit')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)






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




def add_comment_to_movie(request, movie_name):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.film = movie_name
        new_comment.save()
        return redirect('movie_details', movie_name=movie_name)


def edit_profile(request, profile_id):
  profile = Profile.objects.get(id=profile_id)

  if request.method == 'POST':
    profile_form = ProfileForm(request.POST, instance=request.user.profile)
    if profile_form.is_valid:
        profile_form.save()

        return redirect('profile', profile_id=profile_id)
   
  else:
    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile/edit.html', 
    { 
    'profile_form': profile_form,
    })

def delete_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    user = User.objects.get(id = profile.user_id)
    user.delete()
    profile.delete()
    return redirect('home')

  

def movie_show(request):
    movie = Movie()
    
    populars = movie.popular()
    print(populars)

    context ={
        'movie': populars,
    
    }
    return render(request , 'movie/index.html' , context)

def movie_details(request, movie_name):
    comment_form = CommentForm()
    movie = Movie()
    found_movie = movie.search(movie_name)[0]
    poster_path = found_movie.poster_path[1:]
    similar = movie.similar(found_movie.id)
    print(found_movie.id)
    comments = Comment.objects.filter(film=movie_name)
    print(found_movie)
    context = {'movie': found_movie, 
    'comment_form': comment_form, 
    'comments': comments, 
    'poster_path': poster_path,
    'similar': similar}
    return render(request, 'movie/details.html', context)


@login_required
def account_redirect(request):
    return redirect('account-landing', pk=request.user.pk, name=request.user.username)



def profile_new(request):
    error_message = ''
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
    form = ProfileForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'profile/new.html', context)




def add_movie(request, movie_name):
    movie = Movie()
    found_movie = movie.search(movie_name)[0]
    poster_path = found_movie.poster_path[1:]
    print(poster_path)
    new_film = Film(title=movie_name, poster_path=poster_path)
    new_film.save()
    Profile.objects.get(user=request.user).films_list.add(new_film)
    return redirect('/')

def remove_movie(request, profile_id ,film_id,):
    film = Film.objects.get(id=film_id)
    Profile.objects.get(id=profile_id).films_list.remove(film)
    return redirect('profile',  profile_id)





def tv_show(request):
    tv = TV()
    populars = tv.popular()
    print(populars)
    context ={
        'tv': populars,
    }
    return render(request , 'tv/index.html' , context)


def tv_details(request, tv_name):
    comment_form = CommentForm()
    tv = TV()
    found_tv = tv.search(tv_name)[0]
    poster_path = found_tv.poster_path[1:]
    similar = tv.similar(found_tv.id)
    print(found_tv.id)
    comments = Comment.objects.filter(film=tv_name)
    print(found_tv)
    context = {'tv': found_tv, 
    'comment_form': comment_form, 
    'comments': comments, 
    'poster_path': poster_path,
    'similar': similar}
    return render(request, 'tv/details.html', context)



def add_comment_to_tv(request, tv_title):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.film = tv_title
        new_comment.save()
        return redirect('tv_details', tv_title=tv_title)


# another comment