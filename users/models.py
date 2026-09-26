from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Branch(models.TextChoices):
    CSE = 'CSE', 'Computer Science'
    AIE = 'AIE', 'AI & ML'
    ECE = 'ECE', 'Electronics & Comm'
    CCE = 'CCE', 'Computer & Comm'
    CSQC = 'CSQC', 'CS & Quantum Computing'
    AIDS = 'AIDS', 'AI & Data Science'
    EEE = 'EEE', 'Electrical & Electronics'
    ME = 'ME', 'Mechanical'
    CIVIL = 'CIVIL', 'Civil Engineering'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_hosteller = models.BooleanField(default=False)
    branch = models.CharField(max_length=10, choices=Branch.choices, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}\'s Profile'

    @property
    def career_upvotes(self):
        total = self.user.resources.aggregate(total=Sum('upvotes'))['total']
        return total or 0

    @property
    def followers_count(self):
        return self.user.followers.count()

    @property
    def following_count(self):
        return self.user.following.count()


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'follower')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.follower.username} follows {self.user.username}'