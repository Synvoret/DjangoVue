from django.db import models

from .profile import Profile


# CRUD
class Item(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
