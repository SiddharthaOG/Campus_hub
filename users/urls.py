from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('edit/', views.edit_profile, name='edit_profile'),
    path('<str:username>/', views.user_profile, name='profile'),
    path('<str:username>/follow/', views.follow_user, name='follow'),
]