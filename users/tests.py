from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Profile, Follow
from resources.models import Resource


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.profile.bio = 'Test bio'
        self.profile.phone = '+1234567890'
        self.profile.branch = 'CSE'
        self.profile.year = 3
        self.profile.is_hosteller = True
        self.profile.save()
    
    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.bio, 'Test bio')
        self.assertEqual(self.profile.phone, '+1234567890')
        self.assertEqual(self.profile.branch, 'CSE')
        self.assertEqual(self.profile.year, 3)
        self.assertTrue(self.profile.is_hosteller)
    
    def test_career_upvotes_property(self):
        """Test career_upvotes property sums upvotes on user's resources"""
        # Initially 0
        self.assertEqual(self.profile.career_upvotes, 0)
        
        # Create resources with upvotes
        Resource.objects.create(
            title="Resource 1",
            subject="Math",
            semester=1,
            branch="CSE",
            resource_type="Notes",
            external_url="https://example.com/1",
            uploaded_by=self.user,
            upvotes=5
        )
        Resource.objects.create(
            title="Resource 2",
            subject="Physics",
            semester=2,
            branch="CSE",
            resource_type="Notes",
            external_url="https://example.com/2",
            uploaded_by=self.user,
            upvotes=3
        )
        
        self.assertEqual(self.profile.career_upvotes, 8)
    
    def test_followers_following_properties(self):
        """Test followers_count and following_count properties"""
        other_user = User.objects.create_user(username='other', password='pass')
        Follow.objects.create(user=self.user, follower=other_user)
        
        self.assertEqual(self.profile.followers_count, 1)
        self.assertEqual(self.profile.following_count, 0)
        
        Follow.objects.create(user=other_user, follower=self.user)
        self.assertEqual(self.profile.following_count, 1)
    
    def test_str_representation(self):
        self.assertEqual(str(self.profile), "testuser's Profile")


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.profile = Profile.objects.get_or_create(user=self.user)[0]
    
    def test_profile_page_status(self):
        """Test that user profile page returns 200"""
        response = self.client.get(reverse('users:profile', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertTemplateUsed(response, 'users/profile.html')
    
    def test_profile_page_404(self):
        """Test that non-existent user profile returns 404"""
        response = self.client.get(reverse('users:profile', args=['nonexistent']))
        self.assertEqual(response.status_code, 404)
    
    def test_profile_context(self):
        """Test that profile context contains expected data"""
        response = self.client.get(reverse('users:profile', args=['testuser']))
        self.assertIn('profile_user', response.context)
        self.assertIn('profile', response.context)
        self.assertIn('followers_count', response.context)
        self.assertIn('following_count', response.context)
        self.assertEqual(response.context['profile_user'].username, 'testuser')


class FollowTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass123')
    
    def test_follow_requires_login(self):
        """Test that follow requires authentication"""
        response = self.client.post(reverse('users:follow', args=['otheruser']))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_follow_and_unfollow(self):
        """Test follow and unfollow functionality"""
        self.client.login(username='testuser', password='testpass123')
        
        # Follow
        response = self.client.post(reverse('users:follow', args=['otheruser']))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Follow.objects.filter(user=self.other_user, follower=self.user).exists())
        
        # Unfollow
        response = self.client.post(reverse('users:follow', args=['otheruser']))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Follow.objects.filter(user=self.other_user, follower=self.user).exists())
    
    def test_cannot_follow_self(self):
        """Test that users cannot follow themselves"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('users:follow', args=['testuser']))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Follow.objects.filter(user=self.user, follower=self.user).exists())


class EditProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.profile = Profile.objects.get_or_create(user=self.user)[0]
    
    def test_edit_profile_requires_login(self):
        """Test that edit_profile requires authentication"""
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_edit_profile_get(self):
        """Test GET request to edit profile"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit_profile.html')
    
    def test_edit_profile_post_valid(self):
        """Test valid profile update"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('users:edit_profile'), {
            'bio': 'Updated bio',
            'phone': '+1234567890',
            'branch': 'CSE',
            'year': 4,
            'is_hosteller': True
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio')
        self.assertEqual(self.profile.phone, '+1234567890')
        self.assertEqual(self.profile.branch, 'CSE')
        self.assertEqual(self.profile.year, 4)
        self.assertTrue(self.profile.is_hosteller)