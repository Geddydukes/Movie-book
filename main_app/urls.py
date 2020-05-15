from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('accounts/profile/<int:profile_id>', views.profile, name = 'profile'),
    path('accounts/profile/<int:profile_id>/add_photo', views.add_photo, name = 'add_photo'),

    path('accounts/signup', views.signup, name='signup')
]