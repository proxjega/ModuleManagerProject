from django.contrib.auth.models import User

from .models import Module

def create_module(user, data):
    module = Module.objects.create(
        user=user,
        title=data["title"],
        teacher=data["teacher"],
        description=data.get("description", "")
    )
    module.save()
    return module

def register_user(data):
    user = User.objects.create(
        username=data["username"],
        password=data["password1"],
        email=data["email"],
        first_name=data["first_name"],
        last_name=data["last_name"]
    )
    user.save()
    return user