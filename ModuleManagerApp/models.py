from django.db import models
from django.contrib.auth.models import User


class Module(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=200)
    teacher = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title