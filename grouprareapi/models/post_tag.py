from django.db import models
from .tag import Tag
from .post import Post

class PostTag(models.Model):
    """Model that represents a post tag"""
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
