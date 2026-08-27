from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('freelancer', 'Freelancer'),
        ('client', 'Client'),
        ('both', 'Both'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='freelancer')
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True, default='')
    skills = models.JSONField(default=list, blank=True)  # e.g., ['Python', 'Django', 'React']
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_projects = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"