from django.db import models
from .rare_user import RareUser

class Subscription(models.Model):
    """Model that represents a subscription"""
    follower_id = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name='followers')
    author_id = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name='authors')
    created_on = models.DateField()
    ended_on = models.DateField()
