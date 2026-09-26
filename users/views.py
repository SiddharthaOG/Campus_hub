from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from resources.models import Resource
from users.models import Profile, Follow
from users.forms import ProfileForm


def user_profile(request, username):
    """Display a user's public profile page."""
    profile_user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=profile_user)
    
    # Resources uploaded by this user
    user_resources = Resource.objects.filter(uploaded_by=profile_user).order_by('-created_at')
    
    # Follower/following counts
    followers_count = profile.followers_count
    following_count = profile.following_count
    
    # Check if current user is following this profile
    is_following = False
    mutual_followers = []
    
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(user=profile_user, follower=request.user).exists()
        
        # Mutual followers: users who both request.user and profile_user follow
        request_user_following = set(request.user.following.values_list('user_id', flat=True))
        profile_user_following = set(profile_user.following.values_list('user_id', flat=True))
        mutual_ids = request_user_following & profile_user_following
        mutual_followers = User.objects.filter(id__in=mutual_ids)[:5]
    
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'user_resources': user_resources,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'mutual_followers': mutual_followers,
    }
    return render(request, 'users/profile.html', context)


@login_required
def follow_user(request, username):
    """Follow or unfollow a user."""
    if request.method != 'POST':
        return redirect('users:profile', username=username)
    
    profile_user = get_object_or_404(User, username=username)
    
    if profile_user == request.user:
        messages.error(request, 'You cannot follow yourself.')
        return redirect('users:profile', username=username)
    
    follow_obj, created = Follow.objects.get_or_create(
        user=profile_user,
        follower=request.user
    )
    
    if created:
        messages.success(request, f'You are now following {profile_user.username}.')
    else:
        follow_obj.delete()
        messages.success(request, f'You unfollowed {profile_user.username}.')
    
    return redirect('users:profile', username=username)


@login_required
def edit_profile(request):
    """Edit the current user's profile."""
    profile, _ = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile', username=request.user.username)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'users/edit_profile.html', context)