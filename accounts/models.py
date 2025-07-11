# accounts/models.py

from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    USER_ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    bio = models.TextField(blank=True)

    # Optional Student Fields
    student_id = models.CharField(max_length=20, blank=True, null=True)
    enrollment_year = models.IntegerField(blank=True, null=True)

    # Optional Teacher Fields
    department = models.CharField(max_length=100, blank=True, null=True)
    office_location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
