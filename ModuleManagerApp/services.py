from django.contrib.auth.models import User

from .models import Module

def create_module(user, data):
    module = Module.objects.create(
        user=user,
        title=data["title"],
        teacher=data["teacher"],
        description=data.get("description", "")
    )