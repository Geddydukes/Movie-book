from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('accounts/profile/<int:profile_id>', views.profile, name = 'profile'),
    path('accounts/profile/<int:profile_id>/add_photo', views.add_photo, name = 'add_photo'),
    path('accounts/profile/<int:profile_id>/comment/', views.add_comment_to_movie, name='add_comment_to_movie'),
    path('accounts/signup', views.signup, name='signup')
]