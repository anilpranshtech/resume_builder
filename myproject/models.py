from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    THEME_CHOICES = [
        ('classic', 'Classic Blue'),
        ('modern', 'Modern Green'),
        ('dark', 'Dark Mode'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    summary = models.TextField()
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='modern')
    # Add this line for the profile picture
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} - {self.user.username}"

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    start_year = models.IntegerField()
    end_year = models.IntegerField()

class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    description = models.TextField()

class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()