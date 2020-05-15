from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/profile/new', views.new_profile, name='new_profile' ),
    path('accounts/profile/<int:profile_id>', views.profile, name = 'profile'),
    path('accounts/profile/<int:profile_id>/add_photo', views.add_photo, name = 'add_photo'),
    path('movie/<str:movie_name>/comment', views.add_comment_to_movie, name='add_comment_to_movie'),
    path('accounts/signup', views.signup, name='signup'),
    path('accounts/profile/<int:profile_id>/edit', views.edit_profile, name='edit_profile'),
    path('movie/<str:movie_name>', views.movie_details, name='movie_details')
]