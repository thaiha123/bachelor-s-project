from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('profile/<user_id>/', views.profile, name='profile'),
    path('profile_edit', views.profile_edit, name='profile_edit'),
    path('search', views.search, name='search')
]
