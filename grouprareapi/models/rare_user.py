from django.db import models

class RareUser(models.Model):
    """Model that represents an artist"""
    bio = models.CharField(max_length=50)
    profile_image_url = models.CharField(max_length=50)
    created_on = models.DateField()
    active = models.BooleanField()
    uid = models.CharField(max_length=50)
    
