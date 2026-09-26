from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.home, name='home'),
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/add/', views.add_resource, name='add_resource'),
    path('resources/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('resources/<int:pk>/download/', views.download_resource, name='download_resource'),
    path('resources/<int:pk>/upvote/', views.upvote_resource, name='upvote_resource'),
    path('resources/<int:pk>/comment/', views.add_comment, name='add_comment'),
    # Auth URLs
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='resources:home'), name='logout'),
]