from django.db import models
from .rare_user import RareUser
from .category import Category

class Post(models.Model):
    """Model that represents a post"""
    rare_user_id = models.ForeignKey(RareUser, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    approved = models.BooleanField()
    
