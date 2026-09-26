from django.db import models
from django.contrib.auth.models import User


class Resource(models.Model):
    class ResourceType(models.TextChoices):
        NOTES = 'Notes', 'Notes'
        STUDY_MATERIAL = 'Study Material', 'Study Material'
        PREVIOUS_YEAR = 'Previous Year Question Paper', 'Previous Year Question Paper'
        LAB_MANUAL = 'Lab Manual', 'Lab Manual'
        ASSIGNMENT = 'Assignment', 'Assignment'
        REFERENCE = 'Reference Material', 'Reference Material'
        USEFUL_LINK = 'Useful Link', 'Useful Link'
        OTHER = 'Other', 'Other'

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

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="Briefly describe what this resource contains.")
    subject = models.CharField(max_length=100, help_text="e.g., Data Structures, Operating Systems")
    semester = models.PositiveIntegerField(help_text="e.g., 1 to 8")
    branch = models.CharField(max_length=10, choices=Branch.choices)
    resource_type = models.CharField(max_length=50, choices=ResourceType.choices, default=ResourceType.NOTES)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated keywords, e.g., python, algorithms, mid-term")

    file = models.FileField(upload_to='resources/', null=True, blank=True)
    external_url = models.URLField(blank=True, null=True, help_text="Link to Google Drive, GitHub, etc.")

    download_count = models.PositiveIntegerField(default=0)
    upvotes = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='resources')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=80)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author_name} on {self.resource}'