from django.db import models

class Tag(models.Model):
    """Model that represents a tag"""
    label = models.CharField(max_length=50)
